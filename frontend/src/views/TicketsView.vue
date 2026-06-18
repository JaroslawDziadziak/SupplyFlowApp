<template>
  <div class="layout">

    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>SupplyFlow</h1>
        <p class="sidebar-username">{{ currentUser.username }}</p>
        <span class="sidebar-role">{{ roleLabel }}</span>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/tickets" class="nav-item">Tickets</router-link>
      </nav>

      <!-- Ticket filter options -->
      <div class="filter-section">
          <p class="filter-label">Filter by</p>
          <button
            v-for="option in filterOptions"
            :key="option.value"
            :class="['filter-btn', { active: activeFilter === option.value }]"
            @click="activeFilter = option.value"
          >
            {{ option.label }}
          </button>

          <p class="filter-label status-label">Status</p>
          <button
            v-for="option in statusFilterOptions"
            :key="option.value"
            :class="['filter-btn', { active: statusFilter === option.value }]"
            @click="statusFilter = option.value"
          >
            {{ option.label }}
          </button>
      </div>

      <button @click="handleLogout" class="logout-btn">Log out</button>
    </aside>

    <main class="main-content">
      <div class="page-header">
        <div class="header-left">
          <h2>Tickets</h2>
          <span class="ticket-count">{{ filteredTickets.length }} tickets</span>
        </div>
        <button @click="openCreateModal" class="new-ticket-btn">+ New Ticket</button>
      </div>

      <p v-if="loading" class="status-msg">Loading tickets...</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <div v-if="!loading" class="table-wrapper">
        <table class="tickets-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Assigned to</th>
              <th>Created by</th>
            </tr>
          </thead>
          <tbody>
            <!-- Clicking a row opens the detail modal -->
            <tr
              v-for="ticket in filteredTickets"
              :key="ticket.id"
              @click="openDetailModal(ticket)"
              class="clickable-row"
            >
              <td class="id-cell">#{{ ticket.id }}</td>
              <td class="title-cell">{{ ticket.title }}</td>
              <td>
                <span :class="['badge', 'status-' + ticket.status.toLowerCase().replace(' ', '_')]">
                  {{ ticket.status }}
                </span>
              </td>
              <td>
                <span :class="['badge', 'priority-' + ticket.priority.toLowerCase()]">
                  {{ ticket.priority }}
                </span>
              </td>
              <td class="author-cell">{{ ticket.assigned_to_name || '—' }}</td>
              <td class="author-cell">{{ ticket.created_by }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="filteredTickets.length === 0" class="empty-msg">No tickets found.</p>
      </div>
    </main>

    <!-- CREATE TICKET MODAL -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <h3>New Ticket</h3>
        <form @submit.prevent="handleCreateTicket">
          <label>Title</label>
          <input v-model="newTicket.title" type="text" placeholder="Ticket title" required />

          <label>Description</label>
          <textarea v-model="newTicket.description" placeholder="Describe the issue" required></textarea>

          <label>Priority</label>
          <select v-model="newTicket.priority">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>

          <label>Assign to</label>
          <select v-model="newTicket.assigned_to">
            <option :value="null">Unassigned</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>

          <p v-if="modalError" class="error">{{ modalError }}</p>

          <div class="modal-actions">
            <button type="button" @click="showCreateModal = false" class="cancel-btn">Cancel</button>
            <button type="submit" class="submit-btn">Create Ticket</button>
          </div>
        </form>
      </div>
    </div>

    <!-- DETAIL / EDIT MODAL -->
    <div v-if="showDetailModal && selectedTicket" class="modal-overlay" @click.self="closeDetailModal">
      <div class="modal modal-wide">

        <div class="modal-header">
          <h3>Ticket #{{ selectedTicket.id }}</h3>
          <!-- Only the ticket creator can edit it -->
          <button v-if="canEdit" @click="editMode = !editMode" class="edit-toggle-btn">
            {{ editMode ? 'Cancel Edit' : 'Edit' }}
          </button>
        </div>

        <!-- VIEW MODE -->
        <div v-if="!editMode">
          <p class="detail-title">{{ selectedTicket.title }}</p>
          <p class="detail-desc">{{ selectedTicket.description }}</p>

          <div class="detail-meta">
            <span :class="['badge', 'status-' + selectedTicket.status.toLowerCase().replace(' ', '_')]">
              {{ selectedTicket.status }}
            </span>
            <span :class="['badge', 'priority-' + selectedTicket.priority.toLowerCase()]">
              {{ selectedTicket.priority }}
            </span>
            <span class="meta-info">Created by: {{ selectedTicket.created_by }}</span>
            <span class="meta-info">Assigned to: {{ selectedTicket.assigned_to_name || '—' }}</span>
          </div>

          <!-- Ticket lifecycle actions — only the assigned user can change status this way -->
          <div v-if="isAssignedToMe" class="ticket-actions">
            <button
              v-if="selectedTicket.status === 'New'"
              @click="handleStartWorking"
              class="submit-btn small-btn"
            >
              Start Working
            </button>
            <button
              v-if="selectedTicket.status !== 'Closed'"
              @click="handleCloseTicket"
              class="cancel-btn small-btn"
            >
              Close Ticket
            </button>
          </div>

          <!-- Reassign — visible only if ticket is assigned to current user -->
          <div v-if="isAssignedToMe" class="reassign-section">
            <label>Reassign back to</label>
            <select v-model="reassignTo">
              <option :value="null">Select user...</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.username }}
              </option>
            </select>
            <button @click="handleReassign" class="submit-btn small-btn">Reassign</button>
          </div>
        </div>

        <!-- EDIT MODE — only for ticket creator -->
        <div v-if="editMode">
          <label>Title</label>
          <input v-model="editData.title" type="text" />

          <label>Description</label>
          <textarea v-model="editData.description"></textarea>

          <label>Priority</label>
          <select v-model="editData.priority">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>

          <label>Status</label>
          <select v-model="editData.status">
            <option value="New">New</option>
            <option value="In_progress">In Progress</option>
            <option value="Waiting">Waiting</option>
            <option value="Resolved">Resolved</option>
            <option value="Closed">Closed</option>
          </select>

          <label>Assign to</label>
          <select v-model="editData.assigned_to">
            <option :value="null">Unassigned</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>

          <div class="modal-actions">
            <button type="button" @click="editMode = false" class="cancel-btn">Cancel</button>
            <button @click="handleSaveEdit" class="submit-btn">Save Changes</button>
          </div>
        </div>

        <!-- COMMENTS SECTION -->
        <div class="comments-section">
          <h4>Comments ({{ selectedTicket.comments?.length || 0 }})</h4>

          <div v-if="selectedTicket.comments?.length === 0" class="empty-msg small">
            No comments yet.
          </div>

          <div
            v-for="comment in selectedTicket.comments"
            :key="comment.id"
            class="comment"
          >
            <span class="comment-author">{{ comment.author }}</span>
            <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            <p class="comment-content">{{ comment.content }}</p>
          </div>

          <!-- Add comment form -->
          <div class="add-comment">
            <textarea
              v-model="newComment"
              placeholder="Write a comment..."
              rows="2"
            ></textarea>
            <button @click="handleAddComment" class="submit-btn small-btn">Add Comment</button>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// Load current user from localStorage (saved at login)
const currentUser = JSON.parse(localStorage.getItem('current_user') || '{}')

// Formats role to readable label
const roleLabel = computed(() => {
  const labels = {
    logistics: 'Logistics',
    project_manager: 'Project Manager',
    engineer: 'Engineer',
    other: 'Other',
  }
  return labels[currentUser.role] || currentUser.role
})

// All tickets loaded from API
const tickets = ref([])
const loading = ref(true)
const errorMessage = ref('')

// Users list for dropdowns
const users = ref([])

// Sidebar filter — 'all' | 'mine' | 'assigned'
const activeFilter = ref('all')

const filterOptions = [
  { label: 'All Tickets', value: 'all' },
  { label: 'My Created Tickets', value: 'mine' },
  { label: 'Assigned to me', value: 'assigned' },
]

// Status filter — 'all' | 'new' | 'open' | 'closed'
const statusFilter = ref('all')

const statusFilterOptions = [
  { label: 'New Tickets', value: 'new' },
  { label: 'Open Tickets', value: 'open' },
  { label: 'Closed Tickets', value: 'closed' },
  { label: 'All Statuses', value: 'all' },
]

// CREATE MODAL state
const showCreateModal = ref(false)
const modalError = ref('')
const newTicket = ref({ title: '', description: '', priority: 'medium', assigned_to: null })

// DETAIL MODAL state
const showDetailModal = ref(false)
const selectedTicket = ref(null)
const editMode = ref(false)
const editData = ref({})
const newComment = ref('')
const reassignTo = ref(null)

// Computed: filter tickets based on active sidebar filter
const filteredTickets = computed(() => {
  let result = tickets.value

  // Filter by creator / assignee relationship
  if (activeFilter.value === 'mine') {
    result = result.filter(t => t.created_by === currentUser.username)
  } else if (activeFilter.value === 'assigned') {
    result = result.filter(t => t.assigned_to === currentUser.id)
  }

  // Filter by ticket status (lifecycle stage)
  if (statusFilter.value === 'new') {
    result = result.filter(t => t.status === 'New')
  } else if (statusFilter.value === 'open') {
    result = result.filter(t => t.status === 'In_progress')
  } else if (statusFilter.value === 'closed') {
    result = result.filter(t => t.status === 'Closed')
  }

  return result
})

// ── API CALLS ──────────────────────────────────────────────
//Only the creator can edit this ticket
const canEdit = computed(() => {
  return selectedTicket.value?.created_by === currentUser.username
})

// Is this ticket assigned to the current user?
const isAssignedToMe = computed(() => {
  return selectedTicket.value?.assigned_to === currentUser.id
})


async function fetchTickets() {
  try {
    const response = await api.get('/tickets/')
    tickets.value = response.data.results
  } catch (error) {
    errorMessage.value = 'Failed to load tickets.'
  } finally {
    loading.value = false
  }
}

async function fetchUsers() {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Failed to load users:', error)
  }
}

async function handleCreateTicket() {
  modalError.value = ''
  try {
    await api.post('/tickets/', {
      title: newTicket.value.title,
      description: newTicket.value.description,
      priority: newTicket.value.priority,
      assigned_to: newTicket.value.assigned_to,
    })
    showCreateModal.value = false
    newTicket.value = { title: '', description: '', priority: 'medium', assigned_to: null }
    await fetchTickets()
  } catch (error) {
    modalError.value = 'Failed to create ticket.'
  }
}

async function handleSaveEdit() {
  try {
    // PATCH sends only the changed fields, not the whole object
    await api.patch(`/tickets/${selectedTicket.value.id}/`, {
      title: editData.value.title,
      description: editData.value.description,
      priority: editData.value.priority,
      status: editData.value.status,
      assigned_to: editData.value.assigned_to,
    })
    editMode.value = false
    await fetchTickets()
    // Refresh selected ticket data with updated version
    selectedTicket.value = tickets.value.find(t => t.id === selectedTicket.value.id)
  } catch (error) {
    console.error('Failed to save ticket:', error)
  }
}

async function handleReassign() {
  if (!reassignTo.value) return
  try {
    await api.patch(`/tickets/${selectedTicket.value.id}/`, {
      assigned_to: reassignTo.value,
    })
    reassignTo.value = null
    await fetchTickets()
    selectedTicket.value = tickets.value.find(t => t.id === selectedTicket.value.id)
  } catch (error) {
    console.error('Failed to reassign ticket:', error)
  }
}

async function handleStartWorking() {
  try {
    await api.patch(`/tickets/${selectedTicket.value.id}/`, {
      status: 'In_progress',
    })
    await fetchTickets()
    selectedTicket.value = tickets.value.find(t => t.id === selectedTicket.value.id)
  } catch (error) {
    console.error('Failed to update ticket status:', error)
  }
}

async function handleCloseTicket() {
  try {
    await api.patch(`/tickets/${selectedTicket.value.id}/`, {
      status: 'Closed',
    })
    await fetchTickets()
    selectedTicket.value = tickets.value.find(t => t.id === selectedTicket.value.id)
  } catch (error) {
    console.error('Failed to close ticket:', error)
  }
}


async function handleAddComment() {
  if (!newComment.value.trim()) return
  try {
    await api.post('/comments/', {
      ticket: selectedTicket.value.id,
      content: newComment.value,
    })
    newComment.value = ''
    // Refresh ticket to show new comment
    await fetchTickets()
    selectedTicket.value = tickets.value.find(t => t.id === selectedTicket.value.id)
  } catch (error) {
    console.error('Failed to add comment:', error)
  }
}

// ── MODAL HELPERS ──────────────────────────────────────────

function openCreateModal() {
  showCreateModal.value = true
  modalError.value = ''
}

function openDetailModal(ticket) {
  selectedTicket.value = ticket
  // Pre-fill edit form with current ticket data
  editData.value = {
    title: ticket.title,
    description: ticket.description,
    priority: ticket.priority,
    status: ticket.status,
    assigned_to: ticket.assigned_to,
  }
  editMode.value = false
  reassignTo.value = null
  showDetailModal.value = true
}

function closeDetailModal() {
  showDetailModal.value = false
  selectedTicket.value = null
  editMode.value = false
}

// Formats ISO date string to readable format
function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString('pl-PL', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function handleLogout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('current_user')
  router.push('/login')
}

onMounted(() => {
  fetchTickets()
  fetchUsers()
})
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  font-family: 'Poppins', sans-serif;
}

.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #667eea 0%, #c850c0 100%);
  display: flex;
  flex-direction: column;
  padding: 2rem 1.5rem;
  position: fixed;
  height: 100vh;
  box-sizing: border-box;
}

.sidebar-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.sidebar-header h1 {
  color: white;
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.sidebar-username {
  color: rgba(255,255,255,0.7);
  font-size: 0.8rem;
  margin-bottom: 0.15rem;
}

.sidebar-role {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 0.6rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5em;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.nav-item {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: background 0.2s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* Filter buttons in sidebar */
.filter-section {
  flex: 1;
}

.filter-label {
  color: rgba(255,255,255,0.6);
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.5rem;
}

.filter-btn {
  display: block;
  width: 100%;
  text-align: left;
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.75);
  padding: 0.6rem 0.75rem;
  border-radius: 8px;
  font-family: 'Poppins', sans-serif;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 0.25rem;
}

.filter-btn:hover,
.filter-btn.active {
  background: rgba(255,255,255,0.2);
  color: white;
}

.logout-btn {
  background: rgba(255,255,255,0.15);
  color: white;
  border: 1px solid rgba(255,255,255,0.3);
  padding: 0.7rem;
  border-radius: 10px;
  cursor: pointer;
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.logout-btn:hover { background: rgba(255,255,255,0.25); }

/* Main content */
.main-content {
  margin-left: 240px;
  padding: 2.5rem;
  flex: 1;
  background: #f8f7ff;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header-left { display: flex; align-items: center; gap: 1rem; }

.page-header h2 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #1e1b4b;
}

.ticket-count {
  background: #ede9fe;
  color: #7c3aed;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.new-ticket-btn {
  background: linear-gradient(135deg, #667eea, #c850c0);
  color: white;
  border: none;
  padding: 0.65rem 1.25rem;
  border-radius: 10px;
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.new-ticket-btn:hover { opacity: 0.9; }

/* Table */
.table-wrapper {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(102,126,234,0.08);
  overflow: hidden;
}

.tickets-table { width: 100%; border-collapse: collapse; }

.tickets-table th {
  background: #faf9ff;
  color: #6b7280;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 1rem 1.25rem;
  text-align: left;
  border-bottom: 1px solid #f0eeff;
}

.tickets-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f9f8ff;
  font-size: 0.9rem;
  color: #374151;
}

.tickets-table tr:last-child td { border-bottom: none; }

.clickable-row { cursor: pointer; transition: background 0.15s; }
.clickable-row:hover td { background: #f5f3ff; }

.id-cell { color: #9ca3af; font-weight: 600; }
.title-cell { font-weight: 500; color: #1f2937; }
.author-cell { color: #6b7280; }

.badge {
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-new { background: #dbeafe; color: #1d4ed8; }
.status-in_progress { background: #fef3c7; color: #d97706; }
.status-waiting { background: #f3f4f6; color: #6b7280; }
.status-resolved { background: #d1fae5; color: #059669; }
.status-closed { background: #f3f4f6; color: #374151; }
.priority-low { background: #d1fae5; color: #059669; }
.priority-medium { background: #fef3c7; color: #d97706; }
.priority-high { background: #fee2e2; color: #dc2626; }
.priority-urgent { background: #fce7f3; color: #db2777; }

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-wide { max-width: 640px; }

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.modal h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1e1b4b;
}

.edit-toggle-btn {
  background: #ede9fe;
  color: #7c3aed;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-family: 'Poppins', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.modal label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.3rem;
  margin-top: 0.75rem;
}

.modal input,
.modal textarea,
.modal select {
  width: 100%;
  padding: 0.7rem 1rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}

.modal input:focus,
.modal textarea:focus,
.modal select:focus { border-color: #667eea; }

.modal textarea { height: 90px; resize: vertical; }

/* Detail view */
.detail-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.detail-desc {
  color: #6b7280;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 1.25rem;
}

.meta-info {
  font-size: 0.8rem;
  color: #9ca3af;
}

.reassign-section {
  background: #f8f7ff;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.reassign-section label {
  margin: 0;
  white-space: nowrap;
}

.reassign-section select {
  flex: 1;
  min-width: 150px;
}

.status-label { margin-top: 1rem; }

.ticket-actions {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

/* Comments */
.comments-section {
  border-top: 1px solid #f0eeff;
  margin-top: 1.5rem;
  padding-top: 1.25rem;
}

.comments-section h4 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.comment {
  background: #f8f7ff;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.75rem;
}

.comment-author {
  font-weight: 600;
  font-size: 0.85rem;
  color: #5b21b6;
  margin-right: 0.5rem;
}

.comment-date {
  font-size: 0.75rem;
  color: #9ca3af;
}

.comment-content {
  margin-top: 0.4rem;
  font-size: 0.875rem;
  color: #374151;
}

.add-comment {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Shared button styles */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1rem;
}

.cancel-btn {
  padding: 0.65rem 1.25rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  color: #6b7280;
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
  cursor: pointer;
}

.submit-btn {
  padding: 0.65rem 1.25rem;
  background: linear-gradient(135deg, #667eea, #c850c0);
  color: white;
  border: none;
  border-radius: 10px;
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
}

.small-btn { padding: 0.5rem 1rem; font-size: 0.85rem; }

.status-msg { color: #6b7280; }
.error { color: #dc2626; font-size: 0.85rem; margin-bottom: 0.5rem; }
.empty-msg { padding: 2rem; text-align: center; color: #9ca3af; }
.empty-msg.small { padding: 0.5rem 0; }
</style>
