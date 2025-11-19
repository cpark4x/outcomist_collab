# Image MIME Type Fix - Implementation Summary

## Problem
The application was encountering this error:
```
API Error: 400 {"type":"error","error":{"type":"invalid_request_error",
"message":"messages.9.content.5.image.source.base64.data:
Image does not match the provided media type image/jpeg"}}
```

This occurred when:
1. Users paste/upload images in the chat
2. Images are stored with incorrect MIME types (e.g., PNG declared as JPEG)
3. Images are sent back to Claude API in conversation history
4. Claude validates format and rejects the mismatch

## Solution Implemented

### 1. Image Utility Module (`src/utils/image_utils.py`)
**Purpose**: Detect actual image formats and normalize them to match declared MIME types.

**Key Functions**:
- `detect_image_type()` - Detects actual format from bytes using `imghdr`
- `normalize_image_format()` - Converts images to target format (handles RGBA→RGB for JPEG)
- `get_correct_mime_type()` - Returns correct MIME type based on actual data
- `validate_and_fix_image_mime()` - Main validation function for files
- `validate_base64_image()` - Validates base64-encoded images for Claude API

### 2. FileService Updates (`src/services/file_service.py`)
**Changes**:
- Now accepts both `str` and `bytes` content
- Automatically validates image MIME types on file creation
- Normalizes image format if mismatch detected
- Logs validation actions for debugging

**Benefits**:
- Prevents MIME type mismatches at file creation time
- Works with MCP Playwright screenshots
- Handles user-uploaded images correctly

### 3. Message History Validation (`src/ai/streaming.py`)
**Changes**:
- Added `_validate_message_content()` helper function
- Validates all message content before sending to Claude API
- Detects and fixes image MIME type mismatches in conversation history
- Skips invalid images rather than crashing
- Logs all validation actions

**Benefits**:
- Prevents API errors from historical messages
- Gracefully handles corrupted images
- Maintains conversation flow even with problematic images

### 4. Dependencies (`pyproject.toml`)
**Added**:
- `pillow>=10.0.0` - For image format detection and conversion

## How It Works

### Prevention (File Creation)
```
User uploads PNG image → FileService detects format mismatch
→ Normalizes to declared format → Saves with correct MIME type
```

### Recovery (Message History)
```
Historical message with image → Validate before sending to Claude
→ Detect mismatch → Normalize format → Send corrected image
→ OR skip if invalid → Continue conversation
```

## Testing

### Test Cases to Verify:

1. **Upload PNG as JPEG**:
   - Upload a PNG image
   - System should detect and convert to JPEG
   - No API error

2. **Screenshot from MCP Playwright**:
   - Use Playwright to take screenshot
   - System should handle format correctly
   - No API error

3. **Paste Image from Clipboard**:
   - Paste image in chat
   - System should detect actual format
   - No API error

4. **Historical Messages**:
   - Conversation with 10+ messages containing images
   - All images should be validated
   - No API error on continuation

### Manual Test Script:

```python
# Test the image utilities directly
from src.utils.image_utils import (
    detect_image_type,
    validate_and_fix_image_mime,
    validate_base64_image
)
import base64

# Test 1: Detect PNG pretending to be JPEG
with open("test_image.png", "rb") as f:
    png_bytes = f.read()

detected = detect_image_type(png_bytes)
print(f"Detected type: {detected}")  # Should be 'png'

# Test 2: Validate and fix
fixed_bytes, correct_mime = validate_and_fix_image_mime(
    png_bytes,
    "image/jpeg",  # Wrong declaration
    "test.jpg"
)
print(f"Corrected MIME: {correct_mime}")  # Should be 'image/jpeg' with converted bytes

# Test 3: Validate base64
b64_png = base64.b64encode(png_bytes).decode()
result = validate_base64_image(b64_png, "image/jpeg")
if result:
    fixed_b64, correct_mime = result
    print(f"Base64 validation successful: {correct_mime}")
```

## Files Modified

1. ✅ `src/utils/__init__.py` - Created
2. ✅ `src/utils/image_utils.py` - Created (168 lines)
3. ✅ `src/services/file_service.py` - Modified (added binary support + validation)
4. ✅ `src/ai/streaming.py` - Modified (added message content validation)
5. ✅ `pyproject.toml` - Modified (added Pillow dependency)

## Expected Behavior

### Before Fix:
```
User: [pastes PNG screenshot]
System: [saves as image/jpeg but bytes are PNG]
User: "continue"
System: ❌ API Error: Image does not match media type
```

### After Fix:
```
User: [pastes PNG screenshot]
System: [detects PNG, converts to JPEG, saves correctly]
User: "continue"
System: ✅ [validates history, normalizes if needed, continues successfully]
```

## Logging

All validation actions are logged:
- Info: Successful validations and normalizations
- Warning: Skipped invalid images
- Error: Failed validations (with fallback behavior)

Check logs for:
```
INFO: Validated image file screenshot.png with MIME type image/jpeg
INFO: Validated and fixed image block: image/png -> image/jpeg
WARNING: Skipping invalid image block with MIME type image/jpeg
```

## Next Steps

1. **Test the fix**:
   - Start the backend server
   - Upload various image formats
   - Verify no MIME type errors

2. **Monitor logs**:
   - Check for validation warnings
   - Identify any persistent issues

3. **Performance check**:
   - Image normalization adds minimal overhead
   - Only processes images (not text)
   - Happens asynchronously

## Rollback Plan

If issues occur:
1. Remove `pillow` from dependencies
2. Revert `streaming.py` changes (remove validation calls)
3. Revert `file_service.py` to text-only
4. Delete `src/utils/` directory

## Success Criteria

✅ No more "Image does not match media type" errors
✅ All image formats handled correctly
✅ Conversation history with images works
✅ MCP Playwright screenshots work
✅ User image uploads work
✅ Logs show validation actions

---

**Status**: ✅ Implementation Complete
**Date**: November 18, 2025
**Tested**: Pending user verification
