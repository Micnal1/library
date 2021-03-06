
from app import app, db
from app.models import Author, Book ,Hire

@app.shell_context_processor
def make_shell_context():


   return {
       "db": db,
       "Author": Author,
       "Book": Book,
       "Hire":Hire
   }

if __name__ == "__main__":
    app.run(debug=True)
