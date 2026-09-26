;;; export.el --- Export an org-roam-ui snapshot for static hosting -*- lexical-binding: t; -*-

;; Usage:
;;   emacs --batch -l publish/export.el ROAM-DIR ORG-ROAM-UI-DIR OUT-DIR
;;
;; Writes, under OUT-DIR:
;;   graphdata.json   payload of org-roam-ui's `graphdata' websocket message
;;   variables.json   payload of its `variables' message
;;   notes/<id>.org   what its `/node/:id' servlet returns for each node
;; File paths are made relative to ROAM-DIR, so the UI's static mode can
;; resolve note resources under `files/'.
;;
;; The payloads come from org-roam-ui's own functions (loaded from
;; ORG-ROAM-UI-DIR), with the websocket send captured instead, so the
;; snapshot matches what the live UI receives from Emacs.  Missing
;; packages are installed from MELPA into a throwaway `package-user-dir'.

(require 'cl-lib)
(require 'json)
(require 'package)

(pcase-let ((`(,roam-dir ,ui-dir ,out-dir) command-line-args-left))
  (unless (and roam-dir ui-dir out-dir)
    (error "Usage: emacs --batch -l export.el ROAM-DIR ORG-ROAM-UI-DIR OUT-DIR"))
  (setq command-line-args-left nil)
  (defconst export-roam-dir (file-name-as-directory (expand-file-name roam-dir)))
  (defconst export-ui-dir (expand-file-name ui-dir))
  (defconst export-out-dir (file-name-as-directory (expand-file-name out-dir))))

(defconst export-work-dir
  (expand-file-name "org-roam-ui-export/" temporary-file-directory))

;;; Dependencies

(setq package-user-dir (expand-file-name "elpa/" export-work-dir)
      package-archives '(("gnu" . "https://elpa.gnu.org/packages/")
                         ("melpa" . "https://melpa.org/packages/")))
(package-initialize)
(let ((missing (cl-remove-if (lambda (pkg) (locate-library (symbol-name pkg)))
                             '(org-roam websocket simple-httpd))))
  (when missing
    (package-refresh-contents)
    (mapc #'package-install missing)))

(add-to-list 'load-path export-ui-dir)
(require 'org-roam)
(require 'org-roam-ui)

;;; Database

(setq org-roam-directory export-roam-dir
      org-roam-db-location (expand-file-name "org-roam.db" export-work-dir)
      org-roam-dailies-directory "dailies/")
(when (file-exists-p org-roam-db-location)
  (delete-file org-roam-db-location))
(org-roam-db-sync)

;;; Payloads

(defun export--relative (file)
  "Return FILE relative to the roam directory."
  (file-relative-name file export-roam-dir))

(defun export--capture (send)
  "Call SEND and return the payload of the websocket message it sends."
  (let (message)
    (cl-letf (((symbol-function 'websocket-send-text)
               (lambda (_ws text) (setq message text))))
      (funcall send))
    (alist-get 'data (json-parse-string message :object-type 'alist
                                        :array-type 'list
                                        :null-object nil
                                        :false-object :json-false))))

(defun export--write-json (data file)
  "Write DATA as JSON to FILE."
  (with-temp-file file
    (insert (json-encode data))))

(defun export--graphdata ()
  "Return the graph payload with node files relative to the roam directory."
  (let ((data (export--capture #'org-roam-ui--send-graphdata)))
    (dolist (node (alist-get 'nodes data))
      (setf (alist-get 'file node) (export--relative (alist-get 'file node)))
      (when-let* ((file (alist-get 'FILE (alist-get 'properties node))))
        (setf (alist-get 'FILE (alist-get 'properties node))
              (export--relative file))))
    data))

(defun export--note-dirs ()
  "Return the roam subdirectories holding notes, relative with a trailing /."
  (sort (delete-dups
         (cl-loop for file in (org-roam-list-files)
                  for dir = (file-name-directory (export--relative file))
                  when dir collect dir))
        #'string<))

(defun export--variables ()
  "Return the variables payload with paths relative to the roam directory."
  (let ((data (export--capture
               (lambda () (org-roam-ui--send-variables nil)))))
    (setf (alist-get 'roamDir data) ""
          (alist-get 'dailyDir data) org-roam-dailies-directory
          (alist-get 'subDirs data) (export--note-dirs))
    data))

;;; Export

(make-directory (expand-file-name "notes/" export-out-dir) t)
(let ((graphdata (export--graphdata)))
  (export--write-json graphdata (expand-file-name "graphdata.json" export-out-dir))
  (export--write-json (export--variables)
                      (expand-file-name "variables.json" export-out-dir))
  (dolist (node (alist-get 'nodes graphdata))
    (unless (alist-get 'FILELESS (alist-get 'properties node))
      (let ((id (alist-get 'id node)))
        (with-temp-file (expand-file-name (concat "notes/" id ".org") export-out-dir)
          (insert (org-roam-ui--get-text id))))))
  (message "Exported %d nodes and %d links to %s"
           (length (alist-get 'nodes graphdata))
           (length (alist-get 'links graphdata))
           export-out-dir))

;;; export.el ends here
