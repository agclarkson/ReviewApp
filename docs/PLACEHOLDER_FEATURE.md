# Placeholder Text Feature - What's Changed

## ✨ Improvement Made

All text entry fields now have **gray placeholder text** that disappears when you start typing. This makes the interface much cleaner and more intuitive!

## Before vs After

### ❌ Before (Old Version)
- Example text was typed in the field
- You had to delete it before typing
- Could accidentally submit example text
- Looked cluttered

### ✅ After (New Version)
- Gray placeholder text appears when field is empty
- Disappears instantly when you click and start typing
- Reappears if you leave the field empty
- Much cleaner, professional look
- Impossible to accidentally submit placeholder text

## Where You'll See This

### 1. Game Information Section
**Game & Grade:** 
- Placeholder: *"e.g., Premier 1, Senior 2"* (in gray)

**Date:**
- Placeholder: *"2025-01-01"* (current date in gray)

**Result:**
- Placeholder: *"e.g., Home 24-17 Away"* (in gray)

**Referee:**
- Placeholder: *"Your name"* (in gray)

**Coach:**
- Placeholder: *"Coach name (optional)"* (in gray)

### 2. Match Goals Section

**Primary Goal:**
```
What is your main focus for this game? 
e.g., 'Improve accuracy in jackler decisions at breakdown'
```
(Gray text, disappears when you click)

**Secondary Goal:**
```
Your secondary focus area? 
e.g., 'Better positioning at scrum time'
```
(Gray text, disappears when you click)

### 3. Self Reflection Section

**Did I meet my goals?**
```
Think about specific moments... e.g., 'Primary goal met - 
identified 8/10 jackler situations correctly. Secondary goal 
partly met - positioning at scrums good in first half but...'
```

**What went well?**
```
Be specific... e.g., 'Tackle area management strong - clear 
communication on tackler release. Called advantage well when 
Blue under pressure in 34th min...'
```

**Biggest challenge?**
```
Describe the challenge and your solution... e.g., 'Breakdown 
became messy in final 20 mins. Next time I'll be more proactive 
with warnings when I see the trend starting...'
```

**Taking forward?**
```
Your action points... e.g., 'Work on scrum positioning - stay 
wider to see both props. Keep using advantage effectively as 
today showed it helps game flow...'
```

### 4. CRRDF Question Responses

**Every CRRDF answer field:**
```
Be specific with examples, include time stamps if possible, 
describe what you did and the impact it had...
```

## How It Works

1. **Empty field** → Placeholder text shows in gray
2. **Click field** → Placeholder disappears (if it's still the placeholder)
3. **Start typing** → Your text appears in black
4. **Delete everything and click away** → Placeholder comes back
5. **Come back to field** → Your text is still there (placeholders never overwrite your work)

## Technical Details

The app uses custom `PlaceholderEntry` and `PlaceholderText` classes that:
- Show placeholder in gray (#999999)
- Switch to black when you type real content
- Automatically manage focus in/out events
- Use `get_value()` method to ignore placeholder text when saving

## Benefits for Users

### Clearer Interface
- Know exactly what to enter in each field
- See helpful examples without clutter
- Professional, modern look

### Better UX
- No manual deletion needed
- Can't accidentally submit placeholder text
- Visual cue for empty vs filled fields

### Helpful Guidance
- Examples show the level of detail expected
- Prompts remind you what to think about
- Reduces blank page anxiety

## Example User Experience

**Scenario: Entering game information**

1. Open app → See "Game & Grade: *e.g., Premier 1, Senior 2*" in gray
2. Click the field → Gray text disappears, cursor ready
3. Type "Premier 1" → Appears in black
4. Tab to next field → Your "Premier 1" stays, next field shows its placeholder
5. Complete form → All your entries saved, no placeholders included

**Scenario: Self reflection**

1. See question with helpful placeholder
2. Click text area → Placeholder disappears
3. Start with your own thoughts
4. Placeholder examples remind you to be specific
5. Your detailed reflection is saved

## Testing Checklist

When you run the app, verify:
- ✓ All fields show gray placeholder text when empty
- ✓ Placeholder disappears when you click field
- ✓ Your typed text appears in black
- ✓ Placeholder returns if you delete everything and click away
- ✓ Your real content is never replaced by placeholders
- ✓ Exported Excel contains your content, not placeholder text

## Code Quality

The implementation uses:
- Clean object-oriented design
- Proper event handling (FocusIn/FocusOut)
- Color management for visual feedback
- Safe value extraction (get_value() method)
- Consistent behavior across all fields

---

**Result:** A more polished, user-friendly application that guides you through the review process without cluttering the interface! 🎯
