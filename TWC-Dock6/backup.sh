#!/bin/bash
# Backup Jupyter notebooks to host and named volume every hour
rsync -av /tf/notebooks/ /tf/notebooks_backup/
rsync -av /tf/notebooks/ /dock6/host_backups/
