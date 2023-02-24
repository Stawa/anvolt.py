## <span class="emoji">📜</span> Changelog

A notice detailing the changes made in each version of the project will be included in every release.
Please submit an **[issue](https://github.com/Stawa/anvolt.py/issues)** if you believe there is something missing or an error.

### 「0.2.0」 - Feb. 24, 2023

#### New Features

- Discord Music Functions

  - Introducing new enums: `MusicPropertiesEnums`, `MusicEnums`, `MusicPlatform`, `MusicProperty`, `QueueSession`
  - Improved error handling with new error classes: `InvalidChannel`, `InvalidArgument`, `AlreadyConnected`, `NotConnected`, `PlayerAlreadyPaused`, `PlayerNotPaused`, `PlayerEmpty`, `QueueEmpty`
  - Introducing the new music client `AnVoltMusic`

- Discord Event Functions

  - Introducing the new event client `Event` for music and notifications

- Discord Paginator Button Embed

  - Introducing the new `PageEmbed` for better navigation

- Audio Fetcher for Music

  - Introducing the new audio fetcher `AudioStreamFetcher` for improved music performance.

- Twitch Notifier

  - Added a new feature that allows sending notifications to a specific channel, giving users more control over where their notifications go.
  - Introduced two new events: `on_notification_online` and `on_notification_offline`, which notify users when a streamer goes online or offline, respectively.
  - Added `on_notification_error`, an event that sends a notification when the client encounters an error, allowing users to troubleshoot issues more easily.

### 「0.1.6」 - Jan. 25, 2023

<details>
    <summary><span class="emoji">📄</span><b>View Previous Updates</b></summary>

#### New Features

- Introducing new anime-themed `waifu` and `husbando` options in the `Games` feature
- Added `text`, `player`, `character_name`, and `percentage` properties
- Added new enumerations: `ANIGAMES_WAIFU`, `ANIGAMES_HUSBANDO`, `ANIGAMES_SHIPPER`, `ANIGAMES_OPTION_WAIFU`, and `ANIGAMES_OPTION_HUSBANDO` to provide more options

#### Bug Fix

- Fixed an issue where the `Games.truth` function was returning `None` due to a double `.value`
- Fixed a bug where the `original_response` was returning different results when the produce argument was not used.

</details>

### 「0.1.5」 - Jan. 24, 2023

<details>
    <summary><span class="emoji">📄</span><b>View Previous Updates</b></summary>

#### New Features

- Introducing anvolt.notifier.TwitchClient to interact with Twitch API
- Introducing anvolt.models.TwitchModels to handle Twitch models
- Introducing anvolt.notifier.NotifierClient for sending webhook notification

#### Bug Fix

- Fixed an issue that caused an error to be raised when using the produce argument and changing the `status_code` variable to `status_response`

#### Changed Features

- Renamed the `route.py` file to `enums.py` for better organization and clarity.
- Moved the `errors.py` file to the `models.errors` package for better organization and clarity.
- Updated the typing of the `original_response` property from `dict` to `Union[List[Dict], Dict]` to support lists of dictionaries.
- Updated the typing of the `status_response` property from `int` to `Union[List[int], int]` to support lists of integers.
- Changed the return type of the `produce` function from `Union[List[str], Tuple[List[str], bool]]` to `Tuple[List[str], List[dict]]` to return a tuple of lists containing the URLs and responses, respectively.

#### Package Updates

- Updated `setup.py` with new keywords `Operating System :: OS Independent` and `Environment :: Console` to support a wider range of platforms and environments.

</details>

### 「0.1.4」 - Jan. 21, 2023

<details>
    <summary><span class="emoji">📄</span><b>View Previous Updates</b></summary>

#### New Features

- A Command-Line Interface (CLI) has been added for testing and retrieving endpoint lists for specific categories.
  - `anvolt requests -c <category> -e <endpoint>`: Executes a test request to the specified endpoint in the chosen category.
  - `anvolt category-help`: Displays a list of available categories and their respective endpoints.
  - `anvolt save -c <category> -e <endpoint>`: Retrieves an image from the API and saves it to the current directory set in the command prompt

#### Package Updates

- A `requirements.txt` file has been added to manage package dependencies.
- `install_requires`, `entry_points`, `extras_require`, and `keywords` have been added to the package's setup configuration to improve the package's installation and distribution.

</details>

### 「0.1.3」 » Jan. 20, 2023

<details>
    <summary><span class="emoji">📄</span><b>View Previous Updates</b></summary>

#### Added Features

- A new `Games` class has been added, which allows fetching games category from the API.

#### Removed Features

- Imports for `Utils`, `Trivia`, and `Updater` have been removed as they were causing errors.

##### Package Updates

- Additional classifiers, `Typing :: Typed` and `Intended Audience :: Developers`, have been added to the package metadata.

</details>

### 「0.1.2」 » Jan. 18, 2023

<details>
    <summary><span class="emoji">📄</span><b>View Previous Updates</b></summary>

#### New Features

- Added import for Utils, Trivia, and Updater modules to the `anvolt.__init__.py` file to make it more easier to use them across the project

##### Bug Fixes

- Resolved an issue with the status_code on the \_make_request function to ensure it returns the correct status code.

##### Package Updates

- Updated the package description in the `setup.py`

</details>

### 「0.1.1」 » Jan. 17, 2023

<details>
    <summary><span class="emoji">📄</span><b>View Previous Updates</b></summary>
    <i>This version is in alpha or pre-release stage, any identified bugs or issues will be addressed in future updates</i>
</details>
