# Website
This repo is the project for "Foundations of Computer Science".   
Desired domain name: **SaBiSaBi.com** 
# Group members  
Special thanks to my dear teammates. 
+ zyw @SleepinWei
+ lph @lphlch
+ zxy @HiziQ
+ lmq @lmqqqqqq
+ wwx @qwqOscar
+ wxr @wxrlalala
+ wtc @TonyBest318
## division of work 
+ zyw   
  danmaku system: front-end 
+ lph 
  manager of front-end, user-homepage
+ zxy  
  video-play :front-end 
+ lmq     
  website homepage & login page 
+ wwx   
  manager of back-end 
+ wtc   
  login system : back-end,etc. 
+ wxr   
  danmaku system: back-end,etc. 
## Plan
front-end 
- [ ] homepage 
- [ ] user's personal homepage 
- [ ] video page 
- [ ] better nav bars 
- [ ] better homepage design 
- [ ] danmuku 

back-end 
- [ ] login & auth 
- [ ] email sys 
- [ ] migrations 
- [ ] load danmuku
- [ ] views.py (add db operations) 

## Get started 
Our website is based on flask and is managed with flask CLI.   
Launch the web using `flask run` command   
env settings are stored in `.env` file   
require `dotenv` package to set Environement variables.   

## Structure
website
+   **app**
    +   **auth**:all registration related functions are stored here(login,logout etc)
        +   views.py
        +   forms.py
    +   **main**
        +   errors.py: error handlers
        +   forms.py: web forms
        +   views.py: setting routers
    +   **static** 
        +   css 
        +   js 
        +   images 
        +   fonts 
        +   etc. 
    +   **templates**
        +   **auth**:store all registration related templates(current templates are just for tests) 
        +   some html templates here
    +   models.py: database models
+   **migrations**:for database migration 
+   **venv**
+   manager.py: manage app using flask-script 
