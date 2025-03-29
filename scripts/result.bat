CALL python -m src.local_execution.create_folders
CALL python -m src.local_execution.download_document_path
CALL python -m src.local_execution.download_all_documents_and_files
call python -m src.upload_adms_and_images.upload_batch_adms_and_images.src.document_app
