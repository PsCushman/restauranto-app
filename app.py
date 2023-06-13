#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    return '''
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: left;
                    background-color: #f2f2f2;
                }

                h1 {
                    font-family: 'Hanalei Fill', cursive;
                    font-size: 40px;
                    color: #d4af37;
                    margin-top: 50px;
                    text-align: center;
                    text-shadow: 2px 2px #8B4513;
                }

                p {
                    color: #777;
                    font-size: 18px;
                    margin-top: 0; 
                }

                .route {
                    margin-top: 30px;
                    display: inline-block;
                    background-color: #d4af37;
                    color: #fff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                    font-weight: bold;
                    font-family: cursive;
                    border: 2px solid #8B4513;
                    box-shadow: 2px 2px 4px #8B4513;
                }

                .route:hover {
                    background-color: #b38825;
                }

                .directions {
                    color: #777;
                    font-size: 16px;
                    margin-top: 10px;
                }

                .input-box {
                    margin-top: 10px;
                    font-size: 16px;
                    padding: 5px;
                    border-radius: 5px;
                    border: 1px solid #777;
                }
            </style>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Hanalei+Fill&display=swap" rel="stylesheet">
        </head>
        <body>
            <h1>Welcome to the Restauranto App!</h1>
            <p>Available Routes:</p>
            <a class="route" href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br>
            <p class="directions">Returns precipitation data for 12 months (2016-08-23 to 2017-08-23).</p>
            <br>
            <a class="route" href="/api/v1.0/stations">/api/v1.0/stations</a><br>
            <p class="directions">Returns a list of stations.</p>
            <br>
            <a class="route" href="/api/v1.0/tobs">/api/v1.0/tobs</a><br>
            <p class="directions">Returns temperature observations for the most active station in the last 12 months.</p>
            <br>
            <form action="/api/v1.0/start" method="get">
                <label for="start-date">Start Date:</label>
                <input class="input-box" type="text" id="start-date" name="start-date" placeholder="YYYY-MM-DD"><br>
                <input class="route" type="submit" value="Submit">
            </form>
            <p class="directions">Returns the minimum, average, and maximum temperatures after a start date entered in the YYYY-MM-DD format.</p>
            <br>
            <form action="/api/v1.0/start-end" method="get">
                <label for="start-date">Start Date:</label>
                <input class="input-box" type="text" id="start-date" name="start-date" placeholder="YYYY-MM-DD"><br>
                <label for="end-date">End Date:</label>
                <input class="input-box" type="text" id="end-date" name="end-date" placeholder="YYYY-MM-DD"><br>
                <input class="route" type="submit" value="Submit">
            </form>
            <p class="directions">Returns the minimum, average, and maximum temperatures between start and end dates entered in the YYYY-MM-DD format</p>
        </body>
        </html>
    '''

@app.route("/api/v1.0/precipitation")
def precipitation():

# Define the stations route
@app.route("/api/v1.0/stations")

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():

# Define the start route
@app.route("/api/v1.0/<start>")
def start(start):
    

# Define the start-end route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    

# Run the application
if __name__ == "__main__":
    app.run(debug=True)