# Welcome to pdf_crawler!
This is a RESTful API project, which enables you to upload a PDF files, and get data that was excratced from these files.

## Endpoints:
### PDF - includes the following requests: POST, GET, DELETE.

Examples:

```curl --location --request POST 'http://localhost:5000/pdf/file_3' \ ```
```--header 'Content-Type: application/json' \ ```
```--data-raw '{"path": "C:\\Users\\my_user\\Documents\\pdf_crawler\\pdf_files\\file_1.pdf"}'  ```

```curl --location --request GET 'http://localhost:5000/pdf/new_pdf2' \```
```--data-raw ''```

```curl --location --request DELETE 'http://localhost:5000/pdf/file_3' \```
```--data-raw ''```

### Phone - includes the following requests: GET, DELETE.

Examples:

```curl --location --request GET 'http://localhost:5000/phone/0507893675' ```

```curl --location --request DELETE 'http://localhost:5000/phone/0507893675' \ --data-raw '' ```


### PdfList - uses a GET request to get a list of all PDF files

Example:

```curl --location --request GET 'http://localhost:5000/pdfs' ```

### PhoneList - uses a GET request to get a list of all phone numbers

Example:

```curl --location --request GET 'http://localhost:5000/pdfs' ```

The app was developed in Python, using Flask and SQLAlchemy.
I hope you will find it useful.

Thanks,
Naomi
