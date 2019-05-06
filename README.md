# Synthesize (Backend)
Synthesize: Collaborate on assignments with classmates remotely.

Synthesize is an app designed to provide Cornell students an easy way to collaborate on assignments and ask each other questions. The app fetches all the classes currently offered by Cornell and allows users to create an assignment for that class. Users can then join a group chat and anonymously message each other with questions about that specific assignment. Synthesize was designed to help solve the problem many students have - they're enrolled in classes and don't know other students in that class, so they have nobody to work with. Students like to work collaboratively and often learn better that way, and Synthesize creates a platform for this.

Frontend repository: https://github.com/eli-zhang/synthesize

Screenshots\description located in frontend repository.

The backend is written using Flask, a Python framework, and SQLAlchemy, a Python database toolkit. The API spec can be found [here](https://paper.dropbox.com/doc/Synthesize-API-Spec-FCyFQlO0rDT2SzkGlWoh2). We used the API provided by Class Roster to get all classes at Cornell.
