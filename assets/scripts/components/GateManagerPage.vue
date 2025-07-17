<template>
  <div class="gate-manager-page">
    <!-- Header -->
    <div class="header-section">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-8">
            <div class="d-flex align-items-center">
              <!-- Back to Home Button -->
              <button class="btn btn-outline-light me-3" @click="goToHomePage" title="Back to Home Page">
                <i class="fas fa-arrow-left me-2"></i>Home
              </button>
              <h1 class="display-6 fw-bold text-white mb-2">Gate Manager Dashboard</h1>
            </div>
            <p class="text-white-50 mb-0">Manage passenger boarding and gate control</p>
          </div>
          <div class="col-md-4 text-md-end">
            <div class="d-flex align-items-center justify-content-md-end">
              <div class="user-info me-3">
                <small class="d-block text-white-50">Welcome back,</small>
                <strong class="text-white">{{ userData.name || 'Gate Manager' }}</strong>
              </div>
              <div class="user-avatar">
                <i class="fas fa-user-tie"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-4">
      <!-- Quick Stats -->
      <div class="row mb-4">
        <div class="col-md-3 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-primary">
              <i class="fas fa-ticket-alt"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.totalTickets }}</h3>
              <p class="stat-label">Total Tickets</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-success">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.processedTickets }}</h3>
              <p class="stat-label">Boarded Today</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-warning">
              <i class="fas fa-door-open"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.activeGates }}</h3>
              <p class="stat-label">Active Gates</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-info">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.waitingPassengers }}</h3>
              <p class="stat-label">Waiting Passengers</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Controls -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="glass-card">
            <div class="card-body p-4">
              <div class="row g-3 align-items-end">
                <div class="col-md-3">
                  <label class="form-label text-white fw-semibold">Gate Number</label>
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control glass-input"
                      v-model="filters.gateNumber"
                      placeholder="Enter gate number"
                      @input="filterByGate"
                    >
                    <button class="btn btn-outline-light" @click="clearGateFilter" type="button">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </div>
                <div class="col-md-3">
                  <label class="form-label text-white fw-semibold">Flight Number</label>
                  <input
                    type="text"
                    class="form-control glass-input"
                    v-model="filters.flightNumber"
                    placeholder="Flight number"
                    @input="applyFilters"
                  >
                </div>
                <div class="col-md-3">
                  <label class="form-label text-white fw-semibold">Passenger Name</label>
                  <input
                    type="text"
                    class="form-control glass-input"
                    v-model="filters.passengerName"
                    placeholder="Passenger name"
                    @input="applyFilters"
                  >
                </div>
                <div class="col-md-3">
                  <label class="form-label text-white fw-semibold">Status</label>
                  <select class="form-select glass-input" v-model="filters.status" @change="applyFilters">
                    <option value="">All Statuses</option>
                    <option value="upcoming">Upcoming</option>
                    <option value="checked_in">Checked-in</option>
                    <option value="boarded">Boarded</option>
                  </select>
                </div>
              </div>
              <div class="row mt-4">
                <div class="col-12">
                  <div class="d-flex gap-2 flex-wrap">
                    <button class="btn btn-primary" @click="refreshTickets">
                      <i class="fas fa-sync-alt me-2"></i>Refresh
                    </button>
                    <button class="btn btn-outline-light" @click="clearAllFilters">
                      <i class="fas fa-filter me-2"></i>Clear Filters
                    </button>
                    <div class="ms-auto">
                      <span class="text-white-50">
                        Showing {{ filteredTickets.length }} of {{ tickets.length }} tickets
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tickets Table -->
      <div class="row">
        <div class="col-12">
          <div class="glass-card">
            <div class="card-header">
              <h5 class="mb-0 text-white">
                <i class="fas fa-ticket-alt me-2"></i>Passenger Tickets
                <span v-if="filters.gateNumber" class="badge bg-primary ms-2">
                  Gate {{ filters.gateNumber }}
                </span>
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>Ticket ID</th>
                      <th>Passenger</th>
                      <th>Flight</th>
                      <th>Destination</th>
                      <th>Gate</th>
                      <th>Seat</th>
                      <th>Departure</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="ticket in paginatedTickets" :key="ticket.id">
                      <td>
                        <strong class="text-primary">#{{ ticket.ticket_id }}</strong>
                      </td>
                      <td>
                        <div>
                          <strong class="text-white">{{ ticket.passenger_name }}</strong>
                          <br>
                          <small class="text-white-50">{{ ticket.passenger_email }}</small>
                        </div>
                      </td>
                      <td>
                        <div class="d-flex align-items-center">
                          <i class="fas fa-plane text-primary me-2"></i>
                          <strong class="text-white">{{ ticket.flight_number }}</strong>
                        </div>
                      </td>
                      <td>
                        <div class="d-flex align-items-center">
                          <i class="fas fa-map-marker-alt text-success me-2"></i>
                          <span class="text-white">{{ ticket.destination }}</span>
                        </div>
                      </td>
                      <td>
                        <span v-if="ticket.gate" class="badge bg-info">
                          {{ ticket.gate }}
                        </span>
                        <span v-else class="text-white-50">Not Assigned</span>
                      </td>
                      <td>
                        <span class="badge bg-warning text-dark">{{ ticket.seat }}</span>
                      </td>
                      <td>
                        <div class="text-white">{{ formatTime(ticket.departure_time) }}</div>
                        <small class="text-white-50">{{ formatDate(ticket.departure_time) }}</small>
                      </td>
                      <td>
                        <span :class="getStatusBadgeClass(ticket.status)">
                          {{ formatStatusForDisplay(ticket.status) }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button
                            class="btn btn-outline-primary btn-left"
                            @click="viewTicketDetails(ticket)"
                            title="View Details"
                          >
                            <i class="fas fa-eye"></i>
                          </button>
                          <button
                            class="btn btn-success btn-right"
                            @click="processPassenger(ticket)"
                            :disabled="ticket.status !== 'checked_in'"
                            title="Process Passenger"
                          >
                            <i class="fas fa-check"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Pagination -->
              <div class="d-flex justify-content-between align-items-center p-3 border-top border-secondary">
                <div>
                  <span class="text-white-50">
                    Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(currentPage * itemsPerPage, filteredTickets.length) }}
                    of {{ filteredTickets.length }} entries
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Process Passenger Modal -->
    <div class="modal fade" id="processPassengerModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Process Passenger Through Gate</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedTicket">
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>Passenger:</strong> {{ selectedTicket.passenger_name }}
              </div>
              <div class="col-md-6">
                <strong>Flight:</strong> {{ selectedTicket.flight_number }}
              </div>
            </div>
            <div class="row mb-4">
              <div class="col-md-6">
                <strong>Seat:</strong> {{ selectedTicket.seat }}
              </div>
              <div class="col-md-6">
                <strong>Destination:</strong> {{ selectedTicket.destination }}
              </div>
            </div>

            <form @submit.prevent="confirmProcessPassenger">
              <div class="mb-4">
                <label class="form-label fw-semibold">Gate Number <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control glass-input"
                  v-model="processForm.gateNumber"
                  :placeholder="selectedTicket.gate || 'Enter gate number'"
                  required
                >
                <div class="form-text text-white-50">
                  Current assigned gate: {{ selectedTicket.gate || 'Not assigned' }}
                </div>
              </div>

              <div class="mb-3">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="processForm.confirmIdentity"
                    id="confirmIdentity"
                    required
                  >
                  <label class="form-check-label" for="confirmIdentity">
                    I confirm that passenger identity has been verified
                  </label>
                </div>
              </div>

              <div class="mb-3">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="processForm.confirmDocuments"
                    id="confirmDocuments"
                    required
                  >
                  <label class="form-check-label" for="confirmDocuments">
                    I confirm that all travel documents are valid
                  </label>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Cancel</button>
            <button
              type="button"
              class="btn btn-success"
              @click="confirmProcessPassenger"
              :disabled="!selectedTicket || !processForm.confirmIdentity || !processForm.confirmDocuments || !processForm.gateNumber || selectedTicket.status !== 'checked_in'"
            >
              <i class="fas fa-check me-2"></i>Process Passenger
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Ticket Details Modal -->
    <div class="modal fade" id="ticketDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Ticket Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedTicket">
            <div class="row">
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-primary">Passenger Information</h6>
                <table class="table table-dark table-borderless">
                  <tr>
                    <td class="fw-semibold">Name:</td>
                    <td>{{ selectedTicket.passenger_name }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Email:</td>
                    <td>{{ selectedTicket.passenger_email }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Ticket ID:</td>
                    <td><strong class="text-primary">#{{ selectedTicket.ticket_id }}</strong></td>
                  </tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Flight Information</h6>
                <table class="table table-dark table-borderless">
                  <tr>
                    <td class="fw-semibold">Flight:</td>
                    <td>{{ selectedTicket.flight_number }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Destination:</td>
                    <td>{{ selectedTicket.destination }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Gate:</td>
                    <td>{{ selectedTicket.gate || 'Not assigned' }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Seat:</td>
                    <td><span class="badge bg-warning text-dark">{{ selectedTicket.seat }}</span></td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Departure:</td>
                    <td>{{ formatDateTime(selectedTicket.departure_time) }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Status:</td>
                    <td>
                      <span :class="getStatusBadgeClass(selectedTicket.status)">
                        {{ formatStatusForDisplay(selectedTicket.status) }}
                      </span>
                    </td>
                  </tr>
                </table>
              </div>
            </div>

            <div v-if="selectedTicket.processing_history && selectedTicket.processing_history.length > 0" class="mt-4">
              <h6 class="fw-bold mb-3 text-info">Processing History</h6>
              <div class="timeline">
                <div
                  v-for="(history, index) in selectedTicket.processing_history"
                  :key="index"
                  class="timeline-item"
                >
                  <div class="timeline-marker bg-primary"></div>
                  <div class="timeline-content">
                    <div class="d-flex justify-content-between">
                      <strong class="text-white">{{ history.action }}</strong>
                      <small class="text-white-50">{{ formatDateTime(history.timestamp) }}</small>
                    </div>
                    <!-- Notes are now always 'Passenger processed through gate successfully' -->
                    <div class="text-white-50">Passenger checked-in through gate successfully</div>
                    <small class="text-primary">By: {{ history.processed_by }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button
              type="button"
              class="btn btn-success"
              @click="processPassenger(selectedTicket)"
              :disabled="!selectedTicket || selectedTicket.status !== 'checked_in'"
            >
              <i class="fas fa-check me-2"></i>Process Passenger
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GateManagerPage',
  data() {
    return {
      userData: {
        name: '',
        email: '',
        id: '',
        role: ''
      },
      stats: {
        totalTickets: null,
        processedTickets: null,
        activeGates: null,
        waitingPassengers: null
      },
      tickets: [],
      filteredTickets: [],
      selectedTicket: null,
      filters: {
        gateNumber: '',
        flightNumber: '',
        passengerName: '',
        status: 'checked_in' // Default filter changed to 'checked_in'
      },
      processForm: {
        gateNumber: '',
        confirmIdentity: false,
        confirmDocuments: false
      },
      currentPage: 1,
      itemsPerPage: 10,
      // Modal instances
      ticketDetailsModalInstance: null,
      processPassengerModalInstance: null,
    }
  },
  computed: {
    paginatedTickets() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTickets.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredTickets.length / this.itemsPerPage);
    },
    visiblePages() {
      const pages = [];
      const start = Math.max(1, this.currentPage - 2);
      const end = Math.min(this.totalPages, this.currentPage + 2);

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },
    isSelectedTicketProcessed() {
      return this.selectedTicket && this.selectedTicket.status === 'checked_in';
    },
    canProcessPassenger() {
      return this.selectedTicket &&
             this.processForm.confirmIdentity &&
             this.processForm.confirmDocuments &&
             this.processForm.gateNumber &&
             this.selectedTicket.status === 'checked_in';
    }
  },
  watch: {
    'filters.gateNumber'(newVal) {
      if (newVal) {
        this.filterByGate();
      }
    }
  },
  methods: {
    formatTime(dateString) {
      if (!dateString) return 'N/A';
      try {
        return new Date(dateString).toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        console.error('Error formatting time:', error);
        return 'Invalid Date';
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      try {
        return new Date(dateString).toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric'
        });
      } catch (error) {
        console.error('Error formatting date:', error);
        return 'Invalid Date';
      }
    },
    formatDateTime(dateString) {
      if (!dateString) return 'N/A';
      try {
        return new Date(dateString).toLocaleString('en-US', {
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        console.error('Error formatting datetime:', error);
        return 'Invalid Date';
      }
    },
    formatStatusForDisplay(status) {
      if (!status) return 'N/A';
      // Replace underscores with spaces and capitalize first letter of each word
      return status.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
    getStatusBadgeClass(status) {
      if (!status) return 'badge bg-secondary';

      const classes = {
        'upcoming': 'badge bg-warning text-dark',
        'checked_in': 'badge bg-success',
        'boarded': 'badge bg-primary', // Changed from 'boarding' to 'boarded'
        'cancelled': 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
    },
    filterByGate() {
      this.applyFilters();
      if (this.filters.gateNumber) {
        this.processForm.gateNumber = this.filters.gateNumber;
      }
    },
    applyFilters() {
      this.filteredTickets = this.tickets.filter(ticket => {
        if (!ticket) return false;

        const matchesGate = !this.filters.gateNumber ||
          (ticket.gate && ticket.gate.toLowerCase().includes(this.filters.gateNumber.toLowerCase()));

        const matchesFlight = !this.filters.flightNumber ||
          (ticket.flight_number && ticket.flight_number.toLowerCase().includes(this.filters.flightNumber.toLowerCase()));

        const matchesPassenger = !this.filters.passengerName ||
          (ticket.passenger_name && ticket.passenger_name.toLowerCase().includes(this.filters.passengerName.toLowerCase()));

        const matchesStatus = !this.filters.status || ticket.status === this.filters.status;

        return matchesGate && matchesFlight && matchesPassenger && matchesStatus;
      });

      this.currentPage = 1;
    },
    clearGateFilter() {
      this.filters.gateNumber = '';
      this.applyFilters();
    },
    clearAllFilters() {
      this.filters = {
        gateNumber: '',
        flightNumber: '',
        passengerName: '',
        status: ''
      };
      this.applyFilters();
    },
    refreshTickets() {
      console.log('Refreshing tickets...');
      this.applyFilters();
    },
    viewTicketDetails(ticket) {
      if (!ticket) {
        console.error('No ticket provided to viewTicketDetails');
        return;
      }

      this.selectedTicket = ticket;

      // Ensure processPassengerModal is hidden before showing ticketDetailsModal
      if (this.processPassengerModalInstance) {
        this.processPassengerModalInstance.hide();
      }
      if (this.ticketDetailsModalInstance) {
        this.ticketDetailsModalInstance.show();
      }
    },
    processPassenger(ticket) {
      // Only allow processing if the ticket status is 'upcoming'
      if (!ticket || ticket.status !== 'checked_in') {
        console.warn('Cannot process passenger: Ticket is not in "checked_in" status or invalid ticket provided.');
        this.showErrorMessage('This ticket cannot be processed. Only "checked_in" tickets can be checked in.');
        return;
      }

      this.selectedTicket = { ...ticket };

      this.processForm.gateNumber = ticket.gate || this.filters.gateNumber || '';
      this.processForm.confirmIdentity = false;
      this.processForm.confirmDocuments = false;

      // Ensure ticketDetailsModal is hidden before showing processPassengerModal
      if (this.ticketDetailsModalInstance) {
        this.ticketDetailsModalInstance.hide();
      }
      if (this.processPassengerModalInstance) {
        this.processPassengerModalInstance.show();
      }
    },
    async confirmProcessPassenger() {
      if (!this.selectedTicket) {
        console.error('No selected ticket for processing');
        return;
      }

      // Additional check to ensure only 'upcoming' tickets are processed
      if (this.selectedTicket.status !== 'checked_in') {
        this.showErrorMessage('This ticket cannot be processed. Only "checked_in" tickets can be checked in.');
        return;
      }

      if (!this.processForm.confirmIdentity || !this.processForm.confirmDocuments || !this.processForm.gateNumber) {
        alert('Please complete all required fields and confirmations.');
        return;
      }

      const payload = {
        id: this.selectedTicket.id,
        gate: this.processForm.gateNumber
      };

      try {
        const response = await fetch(`/api/boardingpass/`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to process passenger: " + (errorData.detail || "Unknown error"));
          return;
        }

        const updatedTicket = await response.json();

        // 🔄 ОНОВЛЮЄМО локальні дані (Vue state)
        this.selectedTicket.status = 'boarded';
        this.selectedTicket.gate = updatedTicket.gate;

        // Оновити відповідний квиток у загальному списку
        const ticketIndex = this.tickets.findIndex(t => t.id === this.selectedTicket.id);
        if (ticketIndex !== -1) {
          this.tickets[ticketIndex].status = 'boarded';
          this.tickets[ticketIndex].gate = updatedTicket.gate;
        }

        // Оновити статистику
        this.stats.processedTickets++;
        if (this.stats.totalTickets > 0) {
          this.stats.totalTickets--;
        }
        // Зменшити кількість очікуючих пасажирів, якщо це доречно
        if (this.stats.waitingPassengers > 0) {
          this.stats.waitingPassengers--;
        }

        // Додати запис до історії обробки
        if (!this.selectedTicket.processing_history) {
          this.selectedTicket.processing_history = [];
        }
        this.selectedTicket.processing_history.push({
          action: 'Checked-in through gate',
          timestamp: new Date().toISOString(),
          notes: 'Passenger checked-in through gate successfully',
          processed_by: this.userData.name
        });

        // Закрити модальне вікно
        if (this.processPassengerModalInstance) {
          this.processPassengerModalInstance.hide();
        }

        this.applyFilters(); // Re-apply filters to update table view

        console.log(`Processed passenger ${this.selectedTicket.passenger_name} has been successfully checked in through gate ${this.processForm.gateNumber}`);

        this.showSuccessMessage(`Passenger ${this.selectedTicket.passenger_name} has been successfully checked in through gate ${this.processForm.gateNumber}`);
      } catch (error) {
        console.error("Error processing passenger:", error);
        this.showErrorMessage("An error occurred during processing. Please try again.");
      }
    },
    showSuccessMessage(message) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
      `;

      document.body.appendChild(alertDiv);

      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 5000);
    },
    showErrorMessage(message) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
      `;

      document.body.appendChild(alertDiv);

      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 5000);
    },
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    goToHomePage() {
      // This will navigate the browser back to the root of the application.
      // If you have a Vue Router, you would use this.$router.push('/') instead.
      window.location.href = '/';
    }
  },
  async mounted() {
    // Initialize Bootstrap modal instances once
    if (window.bootstrap && window.bootstrap.Modal) {
      this.ticketDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('ticketDetailsModal'));
      this.processPassengerModalInstance = new window.bootstrap.Modal(document.getElementById('processPassengerModal'));
    } else {
      console.warn('Bootstrap Modal not found. Modals may not function correctly.');
    }

    try {
      const userResponse = await fetch('/api/current_user/');
      const userData = await userResponse.json();
      this.isAuthenticated = userData.isAuthenticated;
      this.userData = {
        name: userData.user.name,
        email: userData.user.email,
        id: userData.user.id,
        role: userData.user.role,
      };

      // Assuming /api/get_upcoming_tickets/ can return all tickets,
      // or you would need a different endpoint like /api/get_all_tickets/
      const ticketsResponse = await fetch('/api/get_upcoming_tickets/');
      const ticketsData = await ticketsResponse.json();
      console.log("Fetched ticketsData:", ticketsData);
      this.tickets = ticketsData.tickets || [];
      this.stats = ticketsData.stats || {};
      this.applyFilters(); // Apply default filter on mount
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
}
</script>

<style scoped>
/* Base styles */
.gate-manager-page {
  --color-primary: #6c63ff;
  --color-secondary: #ff6584;
  --color-tertiary: #43cbff;
  --color-success: #00c9a7;
  --color-dark: #1a1a2e;
  --color-light: #f8f9fa;
  color: var(--color-light);
  font-family: 'Poppins', sans-serif;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); /* Main background from HomePage */
}

/* Header Section */
.header-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
  padding: 2rem 0;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

/* Stat Cards (Quick Stats) */
.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.5rem;
  color: white;
}

.stat-icon.bg-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.bg-success {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
}

.stat-icon.bg-warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.bg-info {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.25rem;
  line-height: 1;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin: 0;
}

/* Glass Card Effect (for filters and table) */
.glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 16px; /* Added border-radius */
}

/* Glass Input Styling */
.glass-input {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  backdrop-filter: blur(10px);
  border-radius: 12px; /* Added border-radius */
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.15) !important;
  border-color: var(--color-primary) !important; /* Using --color-primary */
  box-shadow: 0 0 0 0.2rem rgba(108, 99, 255, 0.25) !important; /* Using --color-primary */
  color: white !important;
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.5) !important;
}

.form-select option {
  background-color: var(--color-dark); /* Ensure options are dark */
  color: var(--color-light);
}

/* Card Header */
.card-header {
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
}

/* Table Styling */
.table-dark {
  --bs-table-bg: transparent; /* Make table background transparent */
}

.table-dark th {
  border-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
  padding: 1rem 0.75rem;
}

.table-dark td {
  border-color: rgba(255, 255, 255, 0.05);
  padding: 1rem 0.75rem;
}

/* Updated table hover style with !important for stronger override */
.table-hover tbody tr:hover {
  background-color: rgba(108, 99, 255, 0.15) !important; /* Slightly more opaque primary color tint on hover */
  transition: background-color 0.2s ease;
}

/* Button Styling */
.btn-primary {
  background: linear-gradient(45deg, var(--color-primary), var(--color-tertiary)); /* From HomePage */
  border: none;
  color: white;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(108, 99, 255, 0.4);
  border-radius: 8px; /* Consistent border-radius */
  padding: 0.5rem 1rem; /* Consistent padding */
  font-weight: 600;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(108, 99, 255, 0.6);
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 8px; /* Consistent border-radius */
  padding: 0.5rem 1rem; /* Consistent padding */
  font-weight: 600;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
}

.btn-success {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
  border: none;
  padding: 0.5rem 1rem; /* Consistent padding */
  font-weight: 600;
}

.btn-success:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(86, 171, 47, 0.4);
}

/* Button group specific styles for rounded corners */
.btn-group-sm .btn {
  padding: 0.375rem 0.5rem;
  border-radius: 6px; /* Default for all buttons in group */
}

.btn-group-sm .btn.btn-left {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

/* Adjusted for only two buttons */
.btn-group-sm .btn.btn-right {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

/* Removed .btn-middle as it's no longer needed */

.btn-outline-primary, .btn-outline-warning {
  border-width: 1px;
}

/* Timeline for Processing History */
.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.timeline-marker {
  position: absolute;
  left: -35px;
  top: 5px;
  width: 12px; /* Slightly larger marker */
  height: 12px;
  border-radius: 50%;
}

.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: -29px; /* Adjusted to align with new marker size */
  top: 17px; /* Adjusted to align with new marker size */
  width: 2px;
  height: calc(100% + 10px);
  background: linear-gradient(to bottom, #667eea, rgba(102, 126, 234, 0.3)); /* Gradient line */
}

.timeline-content {
  background: rgba(255, 255, 255, 0.05); /* Glass effect */
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid #667eea;
  backdrop-filter: blur(10px);
}

/* Modal Styling */
.modal-content {
  background: var(--color-dark) !important; /* Ensure dark background */
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header, .modal-footer {
  background: rgba(255, 255, 255, 0.05) !important; /* Ensure header/footer also have glass effect */
  border-color: rgba(255, 255, 255, 0.1);
}

.btn-close-white {
  filter: invert(1); /* Makes the close button white */
}

.form-check-input:checked {
  background-color: #667eea;
  border-color: #667eea;
}

.badge {
  font-size: 0.75rem;
  padding: 0.5em 0.75em;
  border-radius: 6px;
}

/* Pagination Styling */
.pagination .page-link {
  color: var(--color-light);
  border-color: rgba(255, 255, 255, 0.1);
  background-color: transparent;
  transition: all 0.3s ease;
}

.pagination .page-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.pagination .page-item.active .page-link {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .stat-card {
    margin-bottom: 1rem;
  }

  .btn-group {
    flex-direction: column;
    gap: 0.25rem;
  }

  .btn-group .btn {
    border-radius: 6px !important;
  }

  .table-responsive {
    font-size: 0.875rem;
  }
}
</style>
