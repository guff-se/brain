---
title: "https://simonwillison.net/2023/Mar/27/ai-enhanced-development/"
kind: article
party: third
source: pocket
source_id: "pocket:0345"
provenance: extracted
url: "https://simonwillison.net/2023/Mar/27/ai-enhanced-development/"
ingested: 2026-05-13
created: 2023-03-31
tags: []
status: reference
pocket_status: unread
enrichment: original
---

AI-enhanced development makes me more ambitious with my projects
The thing I’m most excited about in our weird new AI-enhanced reality is the way it allows me to be more ambitious with my projects.
As an experienced developer, ChatGPT (and GitHub Copilot) save me an enormous amount of “figuring things out” time. For everything from writing a for loop in Bash to remembering how to make a cross-domain CORS request in JavaScript—I don’t need to even look things up any more, I can just prompt it and get the right answer 80% of the time.
This doesn’t just make me more productive: it lowers my bar for when a project is worth investing time in at all.
In the past I’ve had plenty of ideas for projects which I’ve ruled out because they would take a day—or days—of work to get to a point where they’re useful. I have enough other stuff to build already!
But if ChatGPT can drop that down to an hour or less, those projects can suddenly become viable.
Which means I’m building all sorts of weird and interesting little things that previously I wouldn’t have invested the time in.
I’ll describe my latest one of these mini-projects in detail.
Using ChatGPT to build a system to archive ChatGPT messages
I use ChatGPT a lot, and I want my own archive of conversations I’ve had with it.
There’s no API for retrieving previous conversations at the moment, but if you open up the browser DevTools and watch the network tab you can see it loading JSON any time you navigate to an older conversation.
This gave me an idea for a solution...
What if I could run some JavaScript on the ChatGPT site that grabbed that JSON data and sent it off to my own server?
I couldn’t find the raw data in JavaScript variables available to the console, so I came up with an alternative approach: could I patch the default fetch() function to intercept calls made by the ChatGPT code to that endpoint, and intercept the data that way?
Normally this is where the project would end. Figuring out how to patch fetch() like that is non-trivial—where I’m using the software engineer’s definition of “non-trivial” as meaning “I don’t know how to do that off the top of my head”. I’d have to do some thinking and research! I’m already tempted to drop this idea and work on something else.
But now I have ChatGPT... so I prompted it:
Write a new JavaScript fetch() function which calls the old one but also saves the JSON that is retrieved—if it is used to retrieve JSON—in a window.fetchedData object
It gave me some code, but it wasn’t quite what I wanted. So I added a follow-up prompt:
No I need to replace the old window.fetch() function entirely—I want to patch it so that I can intercept calls made by other existing code
And it produced the following:
// Define a global object to store fetched JSON data window . fetchedData = { } ; // Store a reference to the original fetch function const originalFetch = window . fetch ; // Define a new fetch function that wraps the original fetch window . fetch = async function ( url , options ) { try { // Call the original fetch function const response = await originalFetch ( url , options ) ; // Check if the response has a JSON content type const contentType = response . headers . get ( 'content-type' ) ; if ( contentType && contentType . includes ( 'application/json' ) ) { // If the response is JSON, clone the response so we can read it twice const responseClone = response . clone ( ) ; // Parse the JSON data and save it to the fetchedData object const jsonData = await responseClone . json ( ) ; window . fetchedData [ url ] = jsonData ; } // Return the original response return response ; } catch ( error ) { // Handle any errors that occur during the fetch console . error ( 'Error fetching and saving JSON:' , error ) ; throw error ; } } ;
That’s exactly what I wanted!
I pasted it into the DevTools console on the ChatGPT site and clicked on some links. It worked as intended.
Here’s that full ChatGPT transcript that got me to this point.
So now I have a prototype! I’ve proved to myself that I can intercept the JSON data fetched by ChatGPT’s own web application code.
I only wanted to run my code on requests that matched https://chat.openai.com/backend-api/conversation/... —I could write a regex for that, but I’d have to remember to escape the necessary characters. ChatGPT did that for me too:
const pattern = / ^ https: \/ \/ chat \. openai \. com \/ backend-api \/ conversation \/ / ;
So now I have the key building blocks I need for my solution: I can intercept JSON fetches and then filter to just the data from the endpoint I care about.
But I need CORS support
My plan was to have my intercepting fetch() call POST the JSON data to my own Datasette Cloud instance, similar to how I record scraped Hacker News listings as described in this post about Datasette’s new write API.
One big problem: this means that code running on the chat.openai.com domain needs to POST JSON to another server. And that means the other server needs to be serving CORS headers.
Datasette Cloud doesn’t (yet) support CORS—and I wasn’t about to implement a new production feature there just so I could solve a problem for this prototype.
What I really needed was some kind of CORS proxy... a URL running somewhere which forwards traffic on to Datasette Cloud but adds CORS headers to enable it to be called from elsewhere.
This represents another potential blocking point: do I really want to implement an entire proxy web application just for this little project?
Here’s my next ChatGPT prompt:
Write a web app in python Starlette which has CORS enabled—including for the auth header—and forwards all incoming requests to any path to another server host specified in an environment variable
I like Starlette and I know it has CORS support and is great for writing proxies. I was hopeful that GPT-4 had seen its documentation before the September 2021 cut-off date.
ChatGPT wrote me some very solid code! It used the python-dotenv package though, and I didn’t feel like using that dependency. So I added:
Rewrite that to use os.environ
The exception handling looked wrong to me, so I said:
Catch httpx.HTTPError as the only exception you care about
And after just those three prompts it produced the following:
import os from starlette . applications import Starlette from starlette . middleware import Middleware from starlette . middleware . cors import CORSMiddleware from starlette . routing import Route from starlette . requests import Request from starlette . responses import JSONResponse import httpx TARGET\_SERVER\_HOST = os . environ . get ( "TARGET\_SERVER\_HOST" ) middleware = [ Middleware ( CORSMiddleware , allow\_origins = [ "\*" ], allow\_credentials = True , allow\_methods = [ "\*" ], allow\_headers = [ "\*" ], ) ] app = Starlette ( middleware = middleware ) async def forward\_request ( request : Request ): try : async with httpx . AsyncClient () as client : target\_url = f" { TARGET\_SERVER\_HOST } { request . url . path } " method = request . method headers = dict ( request . headers ) if "host" in headers : del headers [ "host" ] if request . method in [ "POST" , "PUT" , "PATCH" ]: request\_body = await request . json () else : request\_body = None response = await client . request ( method , target\_url , headers = headers , json = request\_body ) return JSONResponse ( response . json (), status\_code = response . status\_code ) except httpx . HTTPError as e : return JSONResponse ({ "error" : str ( e )}, status\_code = 500 ) app . add\_route ( "/{path:path}" , forward\_request , methods = [ "GET" , "POST" , "PUT" , "PATCH" , "DELETE" ]) if \_\_name\_\_ == "\_\_main\_\_" : import uvicorn uvicorn . run ( app , host = "0.0.0.0" , port = 8000 )
I tested this locally... and spotted a bug. It would fail with a 500 error if the incoming request included a content-length header. I fixed that myself by adding this code:
if "content-length" in headers : del headers [ "content-length" ]
My finished code is here. Here’s the ChatGPT transcript.
I deployed this to Vercel using the method described in this TIL—and now I had a working proxy server.
Creating the tables and a token
ChatGPT had got me a long way. The rest of my implementation was now a small enough lift that I could quickly finish it by myself.
I created two tables in my Datasette Cloud instance by executing the following SQL (using the datasette-write plugin):
create table chatgpt\_conversation ( id text primary key , title text , create\_time float, moderation\_results text , current\_node text , plugin\_ids text ); create table chatgpt\_message ( id text primary key , conversation\_id text references chatgpt\_conversation(id), author\_role text , author\_metadata text , create\_time float, content text , end\_turn integer , weight float, metadata text , recipient text );
Then I made myself a Datasette API token with permission to insert-row and update-row just for those two tables, using the new finely grained permissions feature in the 1.0 alpha series.
The last step was to combine this all together into a fetch() function that did the right thing. I wrote this code by hand, using the ChatGPT prototype as a starting point:
const TOKEN = "dstok\_my-token-here" ; // Store a reference to the original fetch function window . originalFetch = window . fetch ; // Define a new fetch function that wraps the original fetch window . fetch = async function ( url , options ) { try { // Call the original fetch function const response = await originalFetch ( url , options ) ; // Check if the response has a JSON content type const contentType = response . headers . get ( "content-type" ) ; if ( contentType && contentType . includes ( "application/json" ) ) { // If the response is JSON, clone the response so we can read it twice const responseClone = response . clone ( ) ; // Parse the JSON data and save it to the fetchedData object const jsonData = await responseClone . json ( ) ; // NOW: if url for https://chat.openai.com/backend-api/conversation/... // do something very special with it const pattern = / ^ https: \/ \/ chat \. openai \. com \/ backend-api \/ conversation \/ ( . \* ) / ; const match = url . match ( pattern ) ; if ( match ) { const conversationId = match [ 1 ] ; console . log ( "conversationId" , conversationId ) ; console . log ( "jsonData" , jsonData ) ; const conversation = { id : conversationId , title : jsonData . title , create\_time : jsonData . create\_time , moderation\_results : JSON . stringify ( jsonData . moderation\_results ) , current\_node : jsonData . current\_node , plugin\_ids : JSON . stringify ( jsonData . plugin\_ids ) , } ; fetch ( "https://starlette-cors-proxy-simonw-datasette.vercel.app/data/chatgpt\_conversation/-/insert" , { method : "POST" , headers : { "Content-Type" : "application/json" , Authorization : `Bearer ${ TOKEN } ` , } , mode : "cors" , body : JSON . stringify ( { row : conversation , replace : true , } ) , } ) . then ( ( d ) => d . json ( ) ) . then ( ( d ) => console . log ( "d" , d ) ) ; const messages = Object . values ( jsonData . mapping ) . filter ( ( m ) => m . message ) . map ( ( message ) => { m = message . message ; let content = "" ; if ( m . content ) { if ( m . content . text ) { content = m . content . text ; } else { content = m . content . parts . join ( "
" ) ; } } return { id : m . id , conversation\_id : conversationId , author\_role : m . author ? m . author . role : null , author\_metadata : JSON . stringify ( m . author ? m . author . metadata : { } ) , create\_time : m . create\_time , content : content , end\_turn : m . end\_turn , weight : m . weight , metadata : JSON . stringify ( m . metadata ) , recipient : m . recipient , } ; } ) ; fetch ( "https://starlette-cors-proxy-simonw-datasette.vercel.app/data/chatgpt\_message/-/insert" , { method : "POST" , headers : { "Content-Type" : "application/json" , Authorization : `Bearer ${ TOKEN } ` , } , mode : "cors" , body : JSON . stringify ( { rows : messages , replace : true , } ) , } ) . then ( ( d ) => d . json ( ) ) . then ( ( d ) => console . log ( "d" , d ) ) ; } } // Return the original response return response ; } catch ( error ) { // Handle any errors that occur during the fetch console . error ( "Error fetching and saving JSON:" , error ) ; throw error ; } } ;
The fiddly bit here was writing the JavaScript that reshaped the ChatGPT JSON into the rows: [array-of-objects] format needed by the Datasette JSON APIs. I could probably have gotten ChatGPT to help with that—but in this case I pasted the SQL schema into a comment and let GitHub Copilot auto-complete parts of the JavaScript for me as I typed it.
And it works
Now I can paste the above block of code into the browser console on chat.openai.com and any time I click on one of my older conversations in the sidebar the fetch() will be intercepted and the JSON data will be saved to my Datasette Cloud instance.
It’s a lot more than just this project
This ChatGPT archiving problem is just one example from the past few months of things I’ve built that I wouldn’t have tackled without AI-assistance.
It took me longer to write this up than it did to implement the entire project from start to finish!
When evaluating if a new technology is worth learning and adopting, I have two criteria:
Does this let me build things that would have been impossible to build without it? Can this reduce the effort required for some projects such that they tip over from “not worth it” to “worth it” and I end up building them?
Large language models like GPT3/4/LLaMA/Claude etc clearly meet both of those criteria—and their impact on point two keeps on getting stronger for me.
Some more examples
Here are a few more examples of projects I’ve worked on recently that wouldn’t have happened without at least some level of AI assistance:
