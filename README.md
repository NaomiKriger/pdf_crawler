# Welcome to pdf_crawler!
This is a RESTful API project, developed in Python/Flask and uses SQLAlchemy.
The app enables you to upload PDF files, and get/delete the data that was extracted from these files by using HTTP requests.

## General Logic / Flow
The app expects the receive PDF files, where each PDF file contains text including phone number(s).
Once a PDF file is being uploaded, using a POST request, the logic of the crawler runs on the file, extracts a list of phones which was contained in the file, and saves the phones to the DB. Then, we can view the data using GET requests, to see the followings:
* for each PDF file - view the list of phones that appeared in it
* for each phone number - view the list of PDF files in which this phone number was mentioned
* view a list of all PDF files
* view a list of all phone numbers
We can also trigger DELETE requests in order to delete a specific phone number or a specific PDF file from the DB

## Endpoints:
### PDF - includes the following requests: POST, GET, DELETE

#### Examples:

```curl --location --request POST 'http://localhost:5000/pdf/file_3' \ --header 'Content-Type: application/json' \ --data-raw '{"path": "C:\\Users\\my_user\\Documents\\pdf_crawler\\pdf_files\\file_1.pdf"}'  ```

```curl --location --request GET 'http://localhost:5000/pdf/new_pdf2' \ --data-raw ''```

```curl --location --request DELETE 'http://localhost:5000/pdf/file_3' \ --data-raw ''```

### Phone - includes the following requests: GET, DELETE

#### Examples:

```curl --location --request GET 'http://localhost:5000/phone/0507893675' \ --data-raw '' ```

```curl --location --request DELETE 'http://localhost:5000/phone/0507893675' \ --data-raw '' ```


### PdfList - uses a GET request to get a list of all PDF files

#### Example:

```curl --location --request GET 'http://localhost:5000/pdfs' \ --data-raw '' ```

### PhoneList - uses a GET request to get a list of all phone numbers

#### Example:

```curl --location --request GET 'http://localhost:5000/pdfs' \ --data-raw '' ```

I hope you will find this app useful.

Thanks,
Naomi
