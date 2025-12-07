# Question 1 - What's the initial prompt you gave to AI to start the implementation?

Act as an expert full stack developer. I want to implement a prototype of a platform for online coding interviews. It should consist of a frontend and a backend. The frontend should be implemented with React+Vite and the backend with Express.js. It should be kept as simple as possible. User should be able to log in and out. For an interview it should be possible to create a link and share it with candidates. to log into that particular session, the candidate should be able to enter the link and log in. There should be a code panel where everyone can edit the code during the interview. Interviewers in the correct session should be able to see the code and how it updated. All logged in users should be displaced in the upper right corner. If a new user joins, the nickname should be updated in the upper right corner and a message should be displayed that a new user joined. there should be a button to execute the code. The execution results should be displaced next to the code panel. If a interviewer or candidate leaves the session, the nickname in the upper right corner should be removed and a message should be displayed that a user left the session. There should be a landing page in which users can create a session and share the link with candidates. 
These are the features of the platform:
1) Create a link and share it with candidates
2) Allow everyone who connects to edit code in the code panel
3) Show real-time updates to all connected users

The frontend and backend should be implemented separately in two folders called frontend and backend. These folders should also include suitable unit tests for the specific part. Let's start with the frontend and create the code for it. Set it up in such a way that the backend can be mocked easily in the tests. Also add the tests for the frontend. make sure everything works properly for the frontend. Make sure it is clean and simple code. Keep in mind it is a prototype and should be kept as simple as possible. 

Add a github workflow for executing the tests for the frontend. Make sure that everything runs successfully and that all functionality in the frontend is tested.

Add a readme file in the frontend folder that describes how the code can be run and tested. Describe the design considerations and the architecture of the frontend. Describe the technologies used and the tools used. Describe the structure of the frontend.

Finally, create an openAPI spec file which should be on the root level of the project tha should define the interface between the frontend and the backend. It should be complete and well documented.

# Question 2 - What's the terminal command you use for executing tests?
`npm test`

# Question 3 - What's the command you have in package.json for npm dev for running both?
`concurrently \"npm run dev:frontend\" \"npm run dev:backend\" --kill-others --prefix-colors auto`

# Question 4 - What's the library for highlighting for JavaScript and Python?
@monaco-editor/react

# Question 5 - Which library did AI use for compiling Python to WASM?
Pyodide


# Question 6 - What's the base image you used for your Dockerfile?
node:20-alpine

# Question 7 - Which service did you use for deployment?
render


The code can be found here: https://github.com/TimBeckerAachen/code-collab-live

To-Do:
- clean documentation
- remove unused files
