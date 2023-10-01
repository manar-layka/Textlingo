# A Django API that performs text translation for both HTML and plain text inputs. 

![Alt text](translator_project/static/images/translator-image.jpg)


## What can do:
- **Text Translation**: Receive input text, translate it using **google-trans** third-party app which use **google-translate** third-party API, and return the translated text to the user.
- **Content Type Specification**: Users can specify the content type of the input text (e.g., HTML, plain text)
- **HTML Handling**: When the input text is in HTML format, preserve all outer tags (such as h1, h2, p, etc.), while translating only the inner text portions. This ensures that the document structure remains intact.
- **User Associations**: Attach translations to specific users so that each user's translations can be tracked and retrieved.

- **Translation Retrieval**: Provide a feature in your API to fetch all translations associated with a particular user.

## Happy Translation!
