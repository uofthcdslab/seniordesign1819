# Database Access

The file `parsing/accessDB.py` is designed to allow easy access to the summation of all data logs, including geo-location.

### Importing the script

First, the script must be in the current path. If you are already operating in the parsing directory, this is not an issue. If you are not, the directory can be added to the path with `sys.path.append(path)`. If you are in the above directory, the passed path should be `parsing`, if you are in a neighboring directory it should be `../parsing`. This may vary on Windows, flipping the slash should probably fix it.

Once the parsing directory is added to the path the script can be imported normally: `import accessDB as db`.

### Using the database

`accessDB.py` contains 2 functions `geoLoc(addr)` and `filter()`.

#### geoLoc(addr)

`geoLoc(addr)` is designed to return the coordinates of a given address, as an array of doubles, if it exists in the database. If the address does not exist in the database, an array of empty strings is returned.

#### filter()

`filter()` is designed to return a filtered selection of the database sorted by date. It has 7 optional arguments as described below.

`startDate` - The first date to begin selecting data at. Passed as a string formatted as `%m/%d/%Y`. Default is an empty string, which implies start at the earliest date.

`endDate` - The first date to no longer select data at. Passed as a string formatted as `%m/%d/%Y`. Default is an empty string, which implies start at the latest date.

`dayOfWeek` - An integer value representing the day of the week to select where 0 is Monday and 6 is Sunday. Default is -1, implying ignore day of the week.

`call` - Call number to select. Passed as a string, must be exact. Default is an empty string, implying ignore call number.

`nature` - Nature to select. Passed as a string, must be exact. Default is an empty string, implying ignore nature.

`status` - Status to select. Passed as a string, must be exact. Default is an empty string, implying ignore status.

`doGeoLoc` - A boolean value defining if data should have geo-location attached. Default is `False`, don't attach geo-location.

### Common use cases

`filter()` - Will return a complete database without geo-location data.

`filter(doGeoLoc=True)` - Will return a complete database with geo-location data.

`filter(call='190082908')` - Will return all instances of call number 190082908.

`geoLoc('1216 S MILLER PARK WA,WMW')` - Will return the coordinates `[43.018567,-87.967236]`.