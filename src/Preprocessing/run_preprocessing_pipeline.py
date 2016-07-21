import Preprocessing.generate_notes
import Preprocessing.filter_for_keywords

# Generate individual notes based on the results from the sql query
print("Calling the note generation module...")
Preprocessing.generate_notes.main()

# Filter full list of documents for keywords (smoking, tobacco), and produce
#  a list of which ones need annotations
print("Calling the keyword filter module")
Preprocessing.filter_for_keywords.main()

print "Done."

