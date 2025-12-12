# Naming Conventions for Quanti-Badger

This document provides guidelines for naming variables, functions, classes, and other code elements in the Quanti-Badger project. Following these conventions will improve code readability and maintainability.

## General Principles

1. **Be Descriptive**: Names should clearly indicate what they represent or do
2. **Be Concise**: Avoid unnecessarily long names while maintaining clarity
3. **Be Consistent**: Follow the same patterns throughout the codebase
4. **Avoid Abbreviations**: Use full words unless the abbreviation is widely recognized (e.g., `url`, `id`, `api`)
5. **Use Domain Language**: Prefer terms that reflect the domain (device scanning, data advertising, privacy control)

## Variable Naming

### Use Descriptive Names

❌ **Bad Examples:**
```javascript
let d = getDeviceData();
let arr = [];
let temp = calculatePrivacyScore();
let x = true;
```

✅ **Good Examples:**
```javascript
let deviceScanResults = getDeviceData();
let advertisedDataPoints = [];
let privacyScore = calculatePrivacyScore();
let isUserConsentGranted = true;
```

### Naming Patterns

- **Boolean variables**: Prefix with `is`, `has`, `should`, or `can`
  - `isDeviceScanned`, `hasUserConsent`, `shouldAdvertiseData`, `canAccessLocation`

- **Arrays/Collections**: Use plural nouns
  - `devices`, `dataPoints`, `permissions`, `scanResults`

- **Constants**: Use UPPER_SNAKE_CASE
  - `MAX_SCAN_ATTEMPTS`, `DEFAULT_PRIVACY_LEVEL`, `API_TIMEOUT_MS`

- **Regular variables**: Use camelCase
  - `deviceId`, `scanDuration`, `privacySettings`

## Function Naming

### Use Action Verbs

Functions should start with a verb that describes what they do.

❌ **Bad Examples:**
```javascript
function data() { }
function device() { }
function privacy(x) { }
function check() { }
```

✅ **Good Examples:**
```javascript
function fetchDeviceData() { }
function scanDevice() { }
function updatePrivacySettings(settings) { }
function validateUserConsent() { }
```

### Common Verb Patterns

- **get/fetch**: Retrieve data
  - `getDeviceInfo()`, `fetchAdvertisingPreferences()`

- **set/update**: Modify data
  - `setPrivacyLevel()`, `updateDataSharingConsent()`

- **is/has/can**: Return boolean values
  - `isDeviceRegistered()`, `hasRequiredPermissions()`, `canAdvertiseData()`

- **calculate/compute**: Perform calculations
  - `calculatePrivacyScore()`, `computeDataRisk()`

- **validate/verify**: Check validity
  - `validateScanResults()`, `verifyUserIdentity()`

- **create/build**: Construct objects
  - `createDeviceProfile()`, `buildAdvertisingPayload()`

- **handle/process**: Handle events or process data
  - `handleScanComplete()`, `processUserPreferences()`

## Class and Module Naming

### Classes

Use PascalCase for class names and be specific about what the class represents.

❌ **Bad Examples:**
```javascript
class Manager { }
class Handler { }
class Data { }
```

✅ **Good Examples:**
```javascript
class DeviceScanner { }
class PrivacySettingsManager { }
class DataAdvertisingController { }
class UserConsentHandler { }
```

### Modules/Files

Use kebab-case for file names that match the primary export.

❌ **Bad Examples:**
- `utils.js`
- `helpers.js`
- `manager.js`

✅ **Good Examples:**
- `device-scanner.js`
- `privacy-settings-manager.js`
- `user-consent-validator.js`
- `data-advertising-service.js`

## Specific to Quanti-Badger Domain

### Device Scanning

```javascript
// Variables
let deviceScanStatus = 'pending';
let scannedDeviceList = [];
let currentScanProgress = 0;

// Functions
function initializeDeviceScan() { }
function getDeviceCapabilities() { }
function updateScanProgress(progress) { }
```

### Data Advertising

```javascript
// Variables
let advertisableDataPoints = [];
let advertisingPreferences = {};
let isDataAdvertisingEnabled = false;

// Functions
function selectDataToAdvertise(dataPoints) { }
function toggleDataAdvertising(enabled) { }
function getAdvertisedDataSummary() { }
```

### User Privacy and Consent

```javascript
// Variables
let userPrivacyLevel = 'standard';
let consentTimestamp = null;
let privacyPolicyVersion = '1.0';

// Functions
function requestUserConsent() { }
function updatePrivacyPreferences(preferences) { }
function hasValidConsent() { }
function revokeDataSharingPermission() { }
```

## Comments and Documentation

Even with descriptive names, complex logic should have comments:

```javascript
/**
 * Scans the device to identify data points that can be advertised
 * based on user privacy preferences and consent settings.
 * 
 * @param {Object} deviceInfo - Information about the device to scan
 * @param {Object} userPreferences - User's privacy and advertising preferences
 * @returns {Array} List of data points approved for advertising
 */
function scanDeviceForAdvertisableData(deviceInfo, userPreferences) {
  // Implementation
}
```

## Refactoring Checklist

When reviewing or refactoring code, check:

- [ ] Do variable names clearly indicate what data they hold?
- [ ] Do function names clearly indicate what action they perform?
- [ ] Are boolean variables prefixed with `is`, `has`, `should`, or `can`?
- [ ] Are collections named with plural nouns?
- [ ] Are constants in UPPER_SNAKE_CASE?
- [ ] Do class names use PascalCase and clearly represent their purpose?
- [ ] Are single-letter variables avoided (except in short loops)?
- [ ] Are abbreviations avoided unless universally recognized?
- [ ] Are domain-specific terms used appropriately?

## Examples of Refactoring

### Example 1: Device Scanning Function

❌ **Before:**
```javascript
function scan(d) {
  let r = [];
  let p = d.props || {};
  for (let i = 0; i < p.length; i++) {
    if (p[i].ok) {
      r.push(p[i]);
    }
  }
  return r;
}
```

✅ **After:**
```javascript
function scanDeviceProperties(device) {
  let approvedProperties = [];
  let deviceProperties = device.properties || {};
  
  for (let i = 0; i < deviceProperties.length; i++) {
    if (deviceProperties[i].isApproved) {
      approvedProperties.push(deviceProperties[i]);
    }
  }
  
  return approvedProperties;
}
```

### Example 2: Privacy Settings

❌ **Before:**
```javascript
let ps = { l: 2, a: true, t: Date.now() };

function setPL(lvl) {
  ps.l = lvl;
}
```

✅ **After:**
```javascript
let privacySettings = {
  level: 2,
  isAdvertisingEnabled: true,
  lastModifiedTimestamp: Date.now()
};

function setPrivacyLevel(privacyLevel) {
  privacySettings.level = privacyLevel;
}
```

## Conclusion

Descriptive naming is an investment in code quality. It makes the codebase:
- Easier to understand for new team members
- Simpler to maintain and debug
- More self-documenting
- Less prone to errors

When in doubt, choose clarity over brevity.
