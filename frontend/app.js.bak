// ============================================================
// Frontend Entry Point — Sphinx-SCA / IntelliMath-AI
// ============================================================
// This file wires together every frontend module and initialises
// Supabase auth, chat history, and the full UI.

import { supabase } from './supabaseClient.js';
import { generateUUID, autoResize, appState } from './lib/helpers.js';
import { initMarkdown } from './lib/markdown.js';
import { initChat, addMessage, handleSend, setChatCallbacks } from './lib/chat.js';
import { initImageUpload } from './lib/imageUpload.js';
import {
    initSidebar,
    initTheme,
    initMode,
    initCalculator,
    initMathToolbar,
    initModals,
    initGraph,
} from './lib/ui.js';

// ── Supabase helpers ──────────────────────────────────────────

async function saveMessageToSupabase(content, sender, imageUrl = null) {
    if (!appState.currentUserId) {
        console.warn('User is not logged in. Message not saved.');
        return;
    }
    const payload = {
        user_id: appState.currentUserId,
        session_id: appState.currentSessionId,
        content,
        sender,
    };
    if (imageUrl) payload.image_url = imageUrl;

    const { data, error } = await supabase.from('messages').insert([payload]);
    if (error) {
        console.error('Error saving message:', error);
        throw error;
    }
    return data;
}

async function fetchUserData(userId) {
    const sidebarHistoryList = document.getElementById('sidebar-history-list');
    try {
        const { data: messages, error } = await supabase
            .from('messages')
            .select('*')
            .eq('user_id', userId)
            .order('created_at', { ascending: false })
            .limit(100);

        if (error) throw error;

        if (!sidebarHistoryList) return;
        sidebarHistoryList.innerHTML = '';

        if (messages && messages.length > 0) {
            const sessions = [];
            const seenSessions = new Set();
            messages.forEach((msg) => {
                if (!msg.session_id) return;
                if (!seenSessions.has(msg.session_id) && msg.sender === 'user') {
                    seenSessions.add(msg.session_id);
                    sessions.push(msg);
                }
            });

            // Read the study session registry tagged by study-mode.js
            let studySessionMap = {};
            try { studySessionMap = JSON.parse(localStorage.getItem('study_sessions') || '{}'); } catch (e) { }

            const topSessions = sessions.slice(0, 15);

            if (topSessions.length > 0) {
                topSessions.forEach((sessionMsg) => {
                    const isStudy = studySessionMap[sessionMsg.session_id] === 'study';
                    const li = document.createElement('li');
                    li.className = 'history-item';

                    if (isStudy) {
                        // Study Mode session → redirect to study-mode.html
                        li.innerHTML = `
                            <a href="study-mode.html?session=${sessionMsg.session_id}" class="history-link" data-session-id="${sessionMsg.session_id}">
                                <span class="material-symbols-outlined" style="font-size:14px;flex-shrink:0;color:var(--primary);">school</span>
                                <span class="history-text"></span>
                            </a>
                        `;
                    } else {
                        // Normal chat → load in-page as before
                        li.innerHTML = `
                            <a href="#" class="history-link" data-session-id="${sessionMsg.session_id}">
                                <span class="material-symbols-outlined" style="font-size:14px;flex-shrink:0;">forum</span>
                                <span class="history-text"></span>
                            </a>
                        `;
                        li.querySelector('.history-link').addEventListener('click', (e) => {
                            e.preventDefault();
                            loadSession(sessionMsg.session_id, sessionMsg.user_id);
                        });
                    }

                    li.querySelector('.history-text').textContent = sessionMsg.content;
                    sidebarHistoryList.appendChild(li);
                });
            } else {
                sidebarHistoryList.innerHTML =
                    '<li style="padding: 10px 12px; font-size: 13px; color: var(--text-muted);">No chats yet</li>';
            }
        } else {
            sidebarHistoryList.innerHTML =
                '<li style="padding: 10px 12px; font-size: 13px; color: var(--text-muted);">No chats yet</li>';
        }
    } catch (error) {
        console.error('Error fetching chat history:', error);
    }
}

async function loadSession(sessionId, _userId) {
    try {
        const mainSidebar = document.getElementById('main-sidebar');
        const sidebarOverlay = document.getElementById('sidebar-overlay');
        if (window.innerWidth <= 768) {
            if (mainSidebar) mainSidebar.classList.remove('mobile-open');
            if (sidebarOverlay) sidebarOverlay.classList.remove('active');
        }

        const { data: messages, error } = await supabase
            .from('messages')
            .select('*')
            .eq('session_id', sessionId)
            .order('created_at', { ascending: true });

        if (error) throw error;

        appState.currentSessionId = sessionId;
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = '';

        if (messages && messages.length > 0) {
            messages.forEach((msg) => {
                addMessage(msg.content, msg.sender, msg.image_url);
            });
        }

        const heroSection = document.querySelector('.hero');
        const chatInterface = document.getElementById('chat-interface');
        const floatingWrapper = document.getElementById('floating-search-wrapper');
        if (heroSection) heroSection.style.display = 'none';
        if (chatInterface) chatInterface.style.display = 'flex';
        if (floatingWrapper) floatingWrapper.style.display = 'flex';
        appState.isChatActive = true;
        document.querySelectorAll('.chat-attach-hide').forEach((el) => el.classList.add('chat-attach-btn-hidden'));

        if (chatInterface) chatInterface.scrollTop = chatInterface.scrollHeight;
    } catch (error) {
        console.error('Error loading session:', error);
        alert('Could not load chat history.');
    }
}

// Expose loadSession globally (called from sidebar history links)
window.loadSession = loadSession;

// ── Main Initialisation ───────────────────────────────────────

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Init rendering engine
    initMarkdown();

    // 2. Provide Supabase callbacks to the chat module
    setChatCallbacks({
        saveMessage: saveMessageToSupabase,
        fetchHistory: () => {
            if (appState.currentUserId) fetchUserData(appState.currentUserId);
        },
    });

    // 3. Init all UI modules
    initSidebar();
    initTheme();
    initMode();
    initCalculator();
    initMathToolbar();
    initModals();
    initGraph();
    initImageUpload();
    initChat();

    // ── Rotating placeholder for main search input ──
    const mainInput = document.getElementById('main-search-input');
    if (mainInput) {
        const placeholders = [
            'Solve x² + 5x + 6 = 0',
            'Find the derivative of sin(x)·eˣ',
            'Integrate ∫ (1/x) dx from 1 to e',
            'Simplify √(50) + 3√(2)',
            'What is the limit of (sin x)/x as x→0?',
            'Factor 2x³ - 6x² + 4x',
        ];
        let placeholderIdx = 0;
        let placeholderInterval;

        function rotatePlaceholder() {
            // Only animate when input is empty & not focused
            if (!mainInput.value && document.activeElement !== mainInput) {
                mainInput.style.transition = 'opacity 0.3s ease';
                mainInput.style.opacity = '0.5';
                setTimeout(() => {
                    placeholderIdx = (placeholderIdx + 1) % placeholders.length;
                    mainInput.placeholder = placeholders[placeholderIdx];
                    mainInput.style.opacity = '1';
                }, 300);
            }
        }

        placeholderInterval = setInterval(rotatePlaceholder, 3500);

        // Pause rotation when input is focused
        mainInput.addEventListener('focus', () => {
            clearInterval(placeholderInterval);
            mainInput.placeholder = 'Type your question here…';
            mainInput.style.opacity = '1';
        });
        mainInput.addEventListener('blur', () => {
            if (!mainInput.value) {
                placeholderInterval = setInterval(rotatePlaceholder, 3500);
            }
        });
    }

    // 4. Supabase Auth — session & user data
    const {
        data: { session },
    } = await supabase.auth.getSession();

    if (session) {
        appState.currentUserId = session.user.id;

        const userMetadata = session.user.user_metadata;
        let firstName = 'User';
        if (userMetadata?.name) {
            firstName = userMetadata.name.split(' ')[0];
        } else if (session.user.email) {
            firstName = session.user.email.split('@')[0];
        }

        const heroTitle = document.querySelector('.hero-title');
        if (heroTitle) heroTitle.textContent = 'Sphinx-SCA Your Personal Math Solver';

        // Hide login, show avatar
        const loginBtn = document.getElementById('nav-login-btn');
        if (loginBtn) loginBtn.style.display = 'none';

        const avatar = document.getElementById('nav-user-avatar');
        if (avatar) {
            avatar.innerHTML = `<img src="user.png" alt="${firstName}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`;
        }

        const profileContainer = document.getElementById('nav-profile-container');
        if (profileContainer) profileContainer.style.display = 'block';

        // Fetch sidebar history
        fetchUserData(session.user.id);

        // Logout handler
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                if (!confirm('Are you sure you want to log out?')) return;
                await supabase.auth.signOut();
                window.location.reload();
            });
        }
    }

    // 5. Suggestion chips
    document.querySelectorAll('.suggestion-chip').forEach((chip) => {
        chip.addEventListener('click', () => {
            const prompt = chip.dataset.prompt;
            const input = document.getElementById('main-search-input');
            if (prompt && input) {
                input.value = prompt;
                autoResize(input);
                input.focus();
            }
        });
    });


    //khairy update from 249 to 269
    //(اضافة خاصية محادثات مود المذاكرة + خاصية الملاحظات والتاسكات )

    // 6. URL ?session= param — auto-load a normal chat session when landing
    //    from dashboard.html or any shared link.
    //    Study Mode sessions are handled by study-mode.html, so we skip those.
    const urlParams = new URLSearchParams(window.location.search);
    const sessionParam = urlParams.get('session');
    if (sessionParam) {
        let studySessionMap = {};
        try { studySessionMap = JSON.parse(localStorage.getItem('study_sessions') || '{}'); } catch (e) { }
        if (studySessionMap[sessionParam] === 'study') {
            // Redirect to study-mode.html — wrong page
            window.location.replace(`study-mode.html?session=${sessionParam}`);
        } else {
            // Load normal chat session after auth settles
            setTimeout(() => loadSession(sessionParam, null), 300);
        }
    }
});

