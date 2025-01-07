;;; .dir_locals.el --- Description -*- lexical-binding: t; -*-
((nil . ((eval . (setq-local
                  org-roam-directory (expand-file-name (locate-dominating-file
                                                        default-directory ".dir-locals.el"))))
         (eval . (setq-local
                  org-roam-db-location (expand-file-name ".cache/org-roam.db"
                                                         org-roam-directory)))
         (org-publish-project-alist . (("second-brain"
                                        :base-directory "."
                                        :publishing-function org-html-publish-to-html
                                        :publishing-directory "../public"
                                        :recursive t)))
         )))

;;; .dir_locals.el ends here
