# Sphinx-SCA — Mobile Responsive Fix Plan
**Based on:** 6 screenshots from real phone testing
**Affected Pages:** index.html, login.html, chat interface
**Priority:** Ordered from most critical to least

---

## Summary of What Was Seen in the Screenshots

Screenshot 1 shows the hero page on mobile where the math keyboard is open and completely covers the input box and the drop zone leaving the user with no way to type. The logo is also missing from the header showing only the text name and hamburger menu.

Screenshot 2 shows the hero page with the logo present and input visible but the entire drop zone takes up too much vertical space on a small screen pushing the input and buttons too low.

Screenshot 3 shows the chat interface on mobile which actually looks decent but the floating input bar sits too far from the bottom and there is a large empty gap between the last message and the input area.

Screenshot 4 shows the login page which looks clean but the input fields have a noticeably light background that clashes with the dark card in dark mode creating an inconsistent look.

Screenshot 5 shows the mode dropdown in light mode on mobile where the dropdown opens but cuts off the first option and only shows Deep Think and Steps partially, the General option is hidden above the visible area.

Screenshot 6 shows the graph bar appearing on the hero page on mobile where the Plot button is cut off completely at the right edge and the bar overlaps and hides the drop zone and input underneath it making both unusable.

---

## Issue 1 — Math Keyboard Covers the Entire Input Area on Mobile

What was seen in Screenshot 1 is that when the math symbol keyboard opens it fills almost the entire screen and the text input and drop zone above it become completely inaccessible. The user has no way to see what they are typing or interact with the input while the keyboard is open.

What needs to be fixed is that the math keyboard on mobile should appear in a compact bottom sheet format with a maximum height of 40 percent of the viewport. It should have a clearly visible close button at the top right. The main input area should stay visible above it and not be hidden behind it. On mobile the keyboard should not be a full-height overlay.

The file to change is style.css inside the media query for max-width 768px where the math-toolbar class needs a max-height and overflow-y scroll applied so it scrolls internally rather than expanding to push everything else off screen.

---

## Issue 2 — Drop Zone Takes Too Much Space on Mobile

What was seen in Screenshots 1 and 2 is that the drag and drop zone for images and PDFs takes up a tall rectangular area on mobile that is unnecessary because drag and drop does not work on mobile phones. The area just shows an icon and text but occupies a large amount of vertical space pushing the actual text input much lower on the screen.

What needs to be fixed is that on mobile screens smaller than 768px the drop zone should collapse to a very small single-line strip of about 36px height showing just the icon and the word Attach. Alternatively it can be replaced entirely on mobile with a small icon button next to the input rather than a full rectangular zone. Drag and drop functionality does not exist on phones so the large zone is wasted space.

The file to change is style.css in the mobile media query for the drop-zone class. The height should be reduced to around 36px to 44px on mobile and the text should be shortened to just one word.

---

## Issue 3 — Logo Missing From Header in Screenshot 1

What was seen in Screenshot 1 is that the header shows only the hamburger menu on the left, the text Sphinx-SCA in the center, and the theme button plus Log In on the right. The logo image that appears in Screenshot 2 and Screenshot 6 is completely absent.

What needs to be fixed is to check why the logo image sometimes fails to render on mobile. The most likely cause is that the logo-icon image has a fixed width and height and on some screen sizes the flex container in the header collapses the image. The logo container should have a minimum width set and the image should never be hidden or collapsed on any screen size including the smallest phones.

The file to check is style.css for the logo-icon and logo-container classes inside the mobile media query, and also index.html to confirm the img tag always has a fallback.

---

## Issue 4 — Graph Bar Cuts Off the Plot Button on Mobile

What was seen in Screenshot 6 is that when the graph input bar appears at the bottom of the screen on mobile the Plot button on the right side is completely cut off outside the viewport. The user can see the input field and partial text but cannot tap the button to plot anything.

What needs to be fixed is that on mobile the graph bar should stack vertically instead of horizontal. The input field should be full width on its own line and the Plot button should be on the next line below it also at full width. The drag handle icon can be hidden on mobile since dragging is not natural on touch screens. The bar should also not overlap the main input card but appear above it cleanly.

The file to change is style.css for the graph-input-bar class inside the mobile media query. It needs flex-direction changed to column on mobile and the input and button should each be 100 percent width.

---

## Issue 5 — Mode Dropdown Is Partially Cut Off on Mobile

What was seen in Screenshot 5 is that when the mode dropdown opens in the chat input bar on mobile the General option at the top is hidden above the visible area of the dropdown. The dropdown opens upward but the top of it goes beyond the screen edge. Only Deep Think and Steps are visible and the user cannot easily reach General.

What needs to be fixed is that the mode dropdown on mobile should open as a bottom sheet or a fixed overlay anchored to the bottom of the screen rather than a floating dropdown that pops upward. Alternatively the dropdown should be constrained so it never exceeds the available screen height and should have a max-height with internal scrolling. The current positioning that works on desktop fails on small phones.

The file to change is style.css for the mode-dropdown-menu class. On mobile it should use position fixed with bottom set to a value above the input bar, with left 0, right 0, and a border radius only on the top.

---

## Issue 6 — Large Empty Gap Between Messages and Input Bar in Chat

What was seen in Screenshot 3 is that the chat interface on mobile has a very large empty black space between the last message and the floating input bar at the bottom. The messages appear at the top third of the screen and then there is a long empty area before the input card appears.

What needs to be fixed is that the chat interface should use flex layout with the messages wrapper taking all available space and the input bar pinned to the bottom. The chat-interface element should be height 100 percent of the available viewport minus the header and the floating wrapper should be position sticky at the bottom with no extra margin or padding creating the gap.

The file to change is style.css for the chat-interface class on mobile. It should have display flex, flex-direction column, and the chat-messages-wrapper should have flex 1 so it fills the space, and the floating-search-wrapper should not have top or bottom margin that creates the empty space.

---

## Issue 7 — Input Field Background Clashes on Login Page

What was seen in Screenshot 4 is that the login page in dark mode shows the email and password input fields with a noticeably light gray or white background while the card itself is dark. This inconsistency makes it look like the inputs belong to a different design and breaks the dark mode experience.

What needs to be fixed is that on dark mode the login input fields should use the dark background variable instead of a hardcoded light color. The login-input class in login.html uses background: var which should pull from the dark theme variables but appears to be falling back to a light value.

The file to change is login.html inside the style tag for the login-input class. The background should use var of bg-primary which in dark mode is the dark color. The same fix applies to signup.html which has the same input styles.

---

## Issue 8 — Input Bar Footer Buttons Too Small to Tap on Mobile

What was seen in Screenshots 1, 2, 3, and 6 is that the toolbar buttons at the bottom of the input card including the calculator icon, the sigma symbol button, the tools grid button, the mode dropdown, and the send button are all quite small and clustered together. On a phone with an average finger size tapping the correct button requires precision that should not be necessary.

What needs to be fixed is that all interactive buttons in the search-footer area should have a minimum tap target of 44 by 44 pixels on mobile as recommended by Apple and Google accessibility guidelines. The buttons currently appear to be around 32 to 36 pixels. The spacing between buttons should also increase to at least 8px to prevent accidental taps on neighboring buttons.

The file to change is style.css in the mobile media query for search-footer, search-tools, and search-actions classes. All icon buttons should have min-width and min-height of 44px on screens below 768px.

---

## Issue 9 — Hero Section Logo and Title Layout Needs Top Spacing Fix

What was seen in Screenshot 6 is that the hero section logo image, the title, and the subtitle are positioned with very little top margin from the header. The logo appears immediately after the header with almost no breathing room. On desktop this may look fine but on mobile the vertical rhythm is too tight.

What needs to be fixed is that the hero-brand-section should have a margin-top on mobile of at least 24px rather than the current spacing that pushes everything too high up. The logo image size on mobile should also be slightly reduced from 80px to around 56px to save vertical space for the more important input area below.

The file to change is style.css for the hero-brand-section and hero-logo-img classes in the mobile media query.

---

## Issue 10 — Disclaimer Text Wraps Awkwardly at Small Widths

What was seen in Screenshot 3 is that the disclaimer text at the very bottom of the chat page reading Sphinx-SCA can make mistakes. Always verify important calculations. wraps across two lines on the small screen and the line break happens mid-sentence in an awkward place.

What needs to be fixed is that on mobile the disclaimer font size should be reduced slightly to 10px or 11px so it fits on one or two clean lines. The padding on each side should also be increased slightly so the text does not sit flush against the screen edge.

The file to change is style.css for the chat-disclaimer class in the mobile media query.

---

## Issue 11 — Mode Dropdown Arrow Button Shows General Option Cut Off

What was seen in Screenshot 5 is related to Issue 5 but is specifically about the selected mode showing a partially visible divider or element above the Deep Think option suggesting the dropdown container is misaligned relative to its trigger button.

What needs to be fixed is that the dropdown should be tested to confirm the max upward positioning does not exceed the screen top. A safe fix is to set the dropdown to never open upward on mobile and instead always open downward or as a bottom sheet so positioning is predictable regardless of screen height.

The file to change is style.css for the mode-dropdown-menu class. An additional attribute of max-height and overflow-y auto should be added.

---

## Fix Priority Order

The issues should be fixed in this order for maximum impact with the least effort.

The first priority is Issue 1 about the math keyboard covering the input because it makes the main feature of the site completely unusable on mobile.

The second priority is Issue 4 about the graph bar cutting off the Plot button because it makes that entire feature broken on mobile.

The third priority is Issue 6 about the large empty gap in chat because it makes the chat experience feel broken and unfinished.

The fourth priority is Issue 5 about the mode dropdown being cut off because it hides important navigation from the user.

The fifth priority is Issue 2 about the drop zone being too large because it pushes important content off screen unnecessarily.

The sixth priority is Issue 7 about the login input background because it creates a visual inconsistency in dark mode.

The seventh priority is Issue 8 about the small tap targets because it affects usability for all users on mobile.

The remaining issues from 3, 9, 10, and 11 are lower priority polish items that should be addressed after the main functional issues are resolved.

---

## Files That Need Changes

style.css needs the majority of the changes specifically inside the existing media query blocks for max-width 768px and a new block for max-width 480px for the smallest phones.

login.html needs a change to the login-input background color in the embedded style tag.

signup.html needs the same change as login.html.

No JavaScript changes are required for any of these fixes. All of them are purely CSS layout and sizing corrections.

---

**Total Issues Found From Screenshots: 11**
Critical Mobile Blockers: 3 — Visual Inconsistencies: 3 — Usability: 3 — Polish: 2
