// ---------- 配置 ----------
const API_BASE = "http://127.0.0.1:8000/api/v1";
let token = localStorage.getItem("token") || "";

if (!token) {
    const userToken = prompt("请输入你的 JWT Token（从 /login 或 /register 获取）:");
    if (userToken) {
        token = userToken;
        localStorage.setItem("token", token);
    }
}

// DOM 元素
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("msg-input");
const sendBtn = document.getElementById("send-btn");
const statusEl = document.getElementById("status");
const sessionList = document.getElementById("session-list");
const newSessionBtn = document.getElementById("new-session-btn");
const sessionTitleEl = document.getElementById("session-title");

let currentSessionId = null;
let isStreaming = false;

// ---------- 工具函数 ----------
function setStatus(text) {
    statusEl.textContent = text;
}

function addMessage(content, role) {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    div.textContent = content;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}

function clearChatBox() {
    chatBox.innerHTML = "";
}

// ---------- 会话管理 ----------
async function loadSessions() {
    try {
        const res = await fetch(`${API_BASE}/sessions`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("获取会话失败");
        const sessions = await res.json();
        renderSessionList(sessions);
        if (sessions.length > 0) {
            const exists = sessions.some(s => s.id === currentSessionId);
            if (!exists || currentSessionId === null) {
                currentSessionId = sessions[0].id;
                sessionTitleEl.textContent = sessions[0].title;
                loadHistory(currentSessionId);
            }
        } else {
            await createSession("新对话");
        }
    } catch (err) {
        setStatus(`加载会话失败: ${err.message}`);
    }
}

function renderSessionList(sessions) {
    sessionList.innerHTML = "";
    sessions.forEach(s => {
        const div = document.createElement("div");
        div.className = `session-item${s.id === currentSessionId ? ' active' : ''}`;
        div.innerHTML = `
            <span>${s.title}</span>
            <button class="delete-btn" data-id="${s.id}">✕</button>
        `;
        div.addEventListener("click", (e) => {
            if (e.target.classList.contains("delete-btn")) return;
            switchSession(s.id);
        });
        const delBtn = div.querySelector(".delete-btn");
        delBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            deleteSession(s.id);
        });
        sessionList.appendChild(div);
    });
}

async function switchSession(sessionId) {
    if (sessionId === currentSessionId) return;
    currentSessionId = sessionId;
    document.querySelectorAll(".session-item").forEach(el => el.classList.remove("active"));
    const activeItem = sessionList.querySelector(`.session-item .delete-btn[data-id="${sessionId}"]`)?.parentElement;
    if (activeItem) activeItem.classList.add("active");
    
    const sessions = await fetch(`${API_BASE}/sessions`, { headers: { Authorization: `Bearer ${token}` } });
    const list = await sessions.json();
    const found = list.find(s => s.id === sessionId);
    if (found) sessionTitleEl.textContent = found.title;
    clearChatBox();
    await loadHistory(sessionId);
}

async function loadHistory(sessionId) {
    try {
        const res = await fetch(`${API_BASE}/users/history?session_id=${sessionId}&limit=50`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("加载历史失败");
        const data = await res.json();
        const history = data.history || [];
        history.forEach(msg => {
            addMessage(msg.message, "user");
            addMessage(msg.reply, "assistant");
        });
        setStatus(`已加载 ${history.length} 条消息`);
    } catch (err) {
        setStatus(`加载历史失败: ${err.message}`);
    }
}

async function createSession(title = "新对话") {
    try {
        const res = await fetch(`${API_BASE}/sessions`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ title }),
        });
        if (!res.ok) throw new Error("创建会话失败");
        const newSession = await res.json();
        await loadSessions();
        await switchSession(newSession.id);
    } catch (err) {
        setStatus(`创建会话失败: ${err.message}`);
    }
}

async function deleteSession(sessionId) {
    if (!confirm("确定要删除此会话及其所有消息吗？")) return;
    try {
        const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("删除失败");
        if (sessionId === currentSessionId) {
            currentSessionId = null;
            clearChatBox();
            sessionTitleEl.textContent = "新对话";
        }
        await loadSessions();
        if (!currentSessionId) {
            await loadSessions();
        }
    } catch (err) {
        setStatus(`删除失败: ${err.message}`);
    }
}

// ---------- 发送消息 ----------
async function sendMessage() {
    const message = input.value.trim();
    if (!message || isStreaming || !currentSessionId) return;

    input.value = "";
    sendBtn.disabled = true;
    isStreaming = true;
    setStatus("AI 正在思考...");

    addMessage(message, "user");

    const aiMsgDiv = document.createElement("div");
    aiMsgDiv.className = "msg assistant";
    aiMsgDiv.textContent = "";
    chatBox.appendChild(aiMsgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    const cursor = document.createElement("span");
    cursor.className = "cursor";
    aiMsgDiv.appendChild(cursor);

    try {
        const response = await fetch(`${API_BASE}/chat/stream`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ message, session_id: currentSessionId, temperature: 0.7 }),
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "请求失败");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let fullText = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n");
            buffer = lines.pop() || "";

            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    const data = line.slice(6);
                    if (data === "[DONE]") {
                        cursor.remove();
                        setStatus("完成");
                        continue;
                    }
                    const textNode = document.createTextNode(data);
                    aiMsgDiv.insertBefore(textNode, cursor);
                    fullText += data;
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            }
        }

        if (cursor.parentNode) cursor.remove();
        setStatus("已完成");
        await loadSessions();
        const sessRes = await fetch(`${API_BASE}/sessions`, { headers: { Authorization: `Bearer ${token}` } });
        const sessList = await sessRes.json();
        const found = sessList.find(s => s.id === currentSessionId);
        if (found) sessionTitleEl.textContent = found.title;

    } catch (err) {
        setStatus(`错误: ${err.message}`);
        aiMsgDiv.textContent = `[错误] ${err.message}`;
        if (cursor.parentNode) cursor.remove();
    }

    sendBtn.disabled = false;
    isStreaming = false;
}

// ---------- 事件绑定 ----------
sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});
newSessionBtn.addEventListener("click", () => {
    createSession("新对话");
});

// ---------- 初始化 ----------
async function init() {
    setStatus("加载会话中...");
    await loadSessions();
}
init();