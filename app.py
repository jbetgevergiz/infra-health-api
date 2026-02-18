import platform
import psutil
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def root():
    # return a JSON object with the api name and version
    # use jsonify() to return dictionaries as JSON
    return jsonify({"api": "System Info API", "version": "1.0"})



@app.route("/health")
def health():   

    return jsonify({"status": "healthy"})


@app.route("/info")
def info():
    
    return jsonify({
        "hostname": platform.node(),
        "os": platform.system(),
        "cpu_usage": psutil.cpu_percent(interval=0.5),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
        "uptime_seconds": int(time.time() - psutil.boot_time())
    })
    # use psutil and platform to grab system data
    # functions i'll use:
    #   platform.node()          -> hostname
    #   platform.system()        -> OS name
    #   psutil.cpu_percent()     -> CPU usage as a float
    #   psutil.virtual_memory()  -> .percent attribute
    #   psutil.disk_usage("/")   -> .percent attribute
    #   psutil.boot_time()       -> system boot time as a timestamp (time.time()-psutil_boot_time() = time since last restart in seconds
    #
    # build a dictionary with these values and return it with jsonify()


if __name__ == "__main__":
    app.run()