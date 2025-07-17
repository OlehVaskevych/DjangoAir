<template>
  <div class="check-in-manager-page">
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
              <h1 class="display-6 fw-bold text-white mb-2">Check-In Manager Dashboard</h1>
            </div>
            <p class="text-white-50 mb-0">Manage passenger check-in and baggage</p>
          </div>
          <div class="col-md-4 text-md-end">
            <div class="d-flex align-items-center justify-content-md-end">
              <div class="user-info me-3">
                <small class="d-block text-white-50">Welcome back,</small>
                <strong class="text-white">{{ userData.name || 'Check-In Manager' }}</strong>
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
              <h3 class="stat-number">{{ stats.checkedInToday }}</h3>
              <p class="stat-label">Checked-in Today</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-warning">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.upcomingPassengers }}</h3>
              <p class="stat-label">Upcoming Passengers</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-info">
              <i class="fas fa-plane-departure"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.flightsToday }}</h3>
              <p class="stat-label">Flights Today</p>
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
                <div class="col-md-4">
                  <label class="form-label text-white fw-semibold">Flight Number</label>
                  <input
                    type="text"
                    class="form-control glass-input"
                    v-model="filters.flightNumber"
                    placeholder="Flight number"
                    @input="applyFilters"
                  >
                </div>
                <div class="col-md-4">
                  <label class="form-label text-white fw-semibold">Passenger Name</label>
                  <input
                    type="text"
                    class="form-control glass-input"
                    v-model="filters.passengerName"
                    placeholder="Passenger name"
                    @input="applyFilters"
                  >
                </div>
                <div class="col-md-4">
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
                            :disabled="ticket.status !== 'upcoming'"
                            title="Process Check-in"
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

    <!-- Process Check-in Modal -->
    <div class="modal fade" id="processCheckInModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Process Passenger Check-in</h5>
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

            <form @submit.prevent="confirmProcessCheckIn">
              <div class="mb-4">
                <label class="form-label fw-semibold">Baggage Weight (kg) <span class="text-danger">*</span></label>
                <input
                  type="number"
                  class="form-control glass-input"
                  v-model.number="processForm.baggageWeight"
                  placeholder="Enter baggage weight"
                  required
                  min="0"
                >
                <div class="form-text text-white-50">
                  Enter the total weight of checked baggage in kilograms.
                </div>
              </div>

              <div class="mb-3">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="processForm.allClear"
                    id="allClear"
                    required
                  >
                  <label class="form-check-label" for="allClear">
                    I confirm all necessary checks have passed (e.g., documents, security)
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
              @click="confirmProcessCheckIn"
              :disabled="!selectedTicket || !processForm.allClear || processForm.baggageWeight === null || selectedTicket.status !== 'upcoming'"
            >
              <i class="fas fa-check me-2"></i>Process Check-in
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
                  <tr v-if="selectedTicket.baggage_weight !== undefined">
                    <td class="fw-semibold">Baggage:</td>
                    <td>{{ selectedTicket.baggage_weight }} kg</td>
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
                    <div class="text-white-50">{{ history.notes }}</div>
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
              :disabled="!selectedTicket || selectedTicket.status !== 'upcoming'"
            >
              <i class="fas fa-check me-2"></i>Process Check-in
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CheckInManagerPage',
  data() {
    return {
      userData: {
        name: 'Jane Doe', // Default name for Check-In Manager
        email: '',
        id: '',
        role: 'check_in_manager'
      },
      stats: {
        totalTickets: null,
        checkedInToday: null, // Renamed from processedTickets
        upcomingPassengers: null, // Renamed from waitingPassengers
        flightsToday: null // New stat
      },
      tickets: [
        {
          id: 1,
          ticket_id: 'TK001234',
          passenger_name: 'John Doe',
          passenger_email: 'john.doe@email.com',
          flight_number: 'DA101',
          destination: 'New York',
          seat: '12A',
          departure_time: '2025-07-18T10:00:00Z',
          status: 'upcoming',
          baggage_weight: null,
          processing_history: []
        },
        {
          id: 2,
          ticket_id: 'TK001235',
          passenger_name: 'Jane Smith',
          passenger_email: 'jane.smith@email.com',
          flight_number: 'DA101',
          destination: 'New York',
          seat: '12B',
          departure_time: '2025-07-18T10:00:00Z',
          status: 'upcoming',
          baggage_weight: null,
          processing_history: []
        },
        {
          id: 3,
          ticket_id: 'TK001236',
          passenger_name: 'Mike Johnson',
          passenger_email: 'mike.johnson@email.com',
          flight_number: 'DA205',
          destination: 'London',
          seat: '8C',
          departure_time: '2025-07-18T12:30:00Z',
          status: 'checked_in',
          baggage_weight: 23.5,
          processing_history: [
            {
              action: 'Checked-in',
              timestamp: '2025-07-18T09:00:00Z',
              notes: 'Baggage 23.5kg, all checks passed',
              processed_by: 'Jane Doe'
            }
          ]
        },
        {
          id: 4,
          ticket_id: 'TK001237',
          passenger_name: 'Sarah Wilson',
          passenger_email: 'sarah.wilson@email.com',
          flight_number: 'DA312',
          destination: 'Paris',
          seat: '15F',
          departure_time: '2025-07-18T14:00:00Z',
          status: 'upcoming',
          baggage_weight: null,
          processing_history: []
        },
        {
          id: 5,
          ticket_id: 'TK001238',
          passenger_name: 'David Brown',
          passenger_email: 'david.brown@email.com',
          flight_number: 'DA101',
          destination: 'New York',
          seat: '12C',
          departure_time: '2025-07-18T10:00:00Z',
          status: 'boarded', // Already boarded, not for check-in manager
          baggage_weight: 18.0,
          processing_history: []
        }
      ],
      filteredTickets: [],
      selectedTicket: null,
      filters: {
        flightNumber: '',
        passengerName: '',
        status: 'upcoming' // Default filter changed to 'upcoming'
      },
      processForm: {
        baggageWeight: null,
        allClear: false
      },
      currentPage: 1,
      itemsPerPage: 10,
      // Modal instances
      ticketDetailsModalInstance: null,
      processCheckInModalInstance: null, // Renamed from processPassengerModalInstance
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
    canProcessCheckIn() {
      return this.selectedTicket &&
             this.processForm.allClear &&
             this.processForm.baggageWeight !== null &&
             this.processForm.baggageWeight >= 0 &&
             this.selectedTicket.status === 'upcoming';
    }
  },
  watch: {
    // No gateNumber filter in check-in manager
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
        'boarded': 'badge bg-primary',
        'cancelled': 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
    },
    applyFilters() {
      this.filteredTickets = this.tickets.filter(ticket => {
        if (!ticket) return false;

        const matchesFlight = !this.filters.flightNumber ||
          (ticket.flight_number && ticket.flight_number.toLowerCase().includes(this.filters.flightNumber.toLowerCase()));

        const matchesPassenger = !this.filters.passengerName ||
          (ticket.passenger_name && ticket.passenger_name.toLowerCase().includes(this.filters.passengerName.toLowerCase()));

        const matchesStatus = !this.filters.status || ticket.status === this.filters.status;

        return matchesFlight && matchesPassenger && matchesStatus;
      });

      this.currentPage = 1;
    },
    clearAllFilters() {
      this.filters = {
        flightNumber: '',
        passengerName: '',
        status: 'upcoming' // Reset to default 'upcoming'
      };
      this.applyFilters();
    },
    refreshTickets() {
      console.log('Refreshing tickets...');
      // In a real app, you would re-fetch data from the server here
      this.applyFilters();
    },
    viewTicketDetails(ticket) {
      if (!ticket) {
        console.error('No ticket provided to viewTicketDetails');
        return;
      }

      this.selectedTicket = ticket;

      // Ensure processCheckInModal is hidden before showing ticketDetailsModal
      if (this.processCheckInModalInstance) {
        this.processCheckInModalInstance.hide();
      }
      if (this.ticketDetailsModalInstance) {
        this.ticketDetailsModalInstance.show();
      }
    },
    processPassenger(ticket) {
      // Only allow processing if the ticket status is 'upcoming'
      if (!ticket || ticket.status !== 'upcoming') {
        console.warn('Cannot process passenger: Ticket is not in "upcoming" status or invalid ticket provided.');
        this.showErrorMessage('This ticket cannot be processed. Only "upcoming" tickets can be checked in.');
        return;
      }

      this.selectedTicket = { ...ticket };

      // Reset form for new processing
      this.processForm.baggageWeight = null;
      this.processForm.allClear = false;

      // Ensure ticketDetailsModal is hidden before showing processCheckInModal
      if (this.ticketDetailsModalInstance) {
        this.ticketDetailsModalInstance.hide();
      }
      if (this.processCheckInModalInstance) {
        this.processCheckInModalInstance.show();
      }
    },
    async confirmProcessCheckIn() { // Renamed from confirmProcessPassenger
      if (!this.selectedTicket) {
        console.error('No selected ticket for processing');
        return;
      }

      // Additional check to ensure only 'upcoming' tickets are processed
      if (this.selectedTicket.status !== 'upcoming') {
        this.showErrorMessage('This ticket cannot be processed. Only "upcoming" tickets can be checked in.');
        return;
      }

      if (!this.processForm.allClear || this.processForm.baggageWeight === null || this.processForm.baggageWeight < 0) {
        alert('Please complete all required fields and confirmations, and ensure baggage weight is valid.');
        return;
      }

      const payload = {
        id: this.selectedTicket.id,
        baggage_weight: this.processForm.baggageWeight,
        all_clear: this.processForm.allClear
      };

      try {
        // Assuming a new API endpoint for check-in
        const response = await fetch(`/api/confirm-checkedin/`, {
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
          this.showErrorMessage("Failed to process check-in: " + (errorData.detail || "Unknown error"));
          return;
        }

        const updatedTicket = await response.json();

        // 🔄 ОНОВЛЮЄМО локальні дані (Vue state)
        this.selectedTicket.status = 'checked_in'; // Status changes to checked_in
        this.selectedTicket.baggage_weight = updatedTicket.baggage_weight;

        // Оновити відповідний квиток у загальному списку
        const ticketIndex = this.tickets.findIndex(t => t.id === this.selectedTicket.id);
        if (ticketIndex !== -1) {
          this.tickets[ticketIndex].status = 'checked_in';
          this.tickets[ticketIndex].baggage_weight = updatedTicket.baggage_weight;
        }

        // Оновити статистику
        this.stats.checkedInToday++;
        if (this.stats.upcomingPassengers > 0) {
          this.stats.upcomingPassengers--;
        }

        // Додати запис до історії обробки
        if (!this.selectedTicket.processing_history) {
          this.selectedTicket.processing_history = [];
        }
        this.selectedTicket.processing_history.push({
          action: 'Checked-in',
          timestamp: new Date().toISOString(),
          notes: `Baggage ${this.processForm.baggageWeight}kg, all checks passed`,
          processed_by: this.userData.name
        });

        // Закрити модальне вікно
        if (this.processCheckInModalInstance) {
          this.processCheckInModalInstance.hide();
        }

        this.applyFilters(); // Re-apply filters to update table view

        console.log(`Processed check-in for passenger ${this.selectedTicket.passenger_name}. Baggage: ${this.processForm.baggageWeight}kg`);

        this.showSuccessMessage(`Passenger ${this.selectedTicket.passenger_name} has been successfully checked in.`);
      } catch (error) {
        console.error("Error processing check-in:", error);
        this.showErrorMessage("An error occurred during check-in. Please try again.");
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
      window.location.href = '/';
    },
    // Helper to calculate initial stats based on mock data
    calculateInitialStats() {
      const today = new Date().toISOString().split('T')[0];
      let total = 0;
      let checkedIn = 0;
      let upcoming = 0;
      let flights = new Set();

      this.tickets.forEach(ticket => {
        total++;
        if (ticket.status === 'checked_in') {
          checkedIn++;
        } else if (ticket.status === 'upcoming') {
          upcoming++;
        }
        if (ticket.departure_time && ticket.departure_time.startsWith(today)) {
          flights.add(ticket.flight_number);
        }
      });

      this.stats.totalTickets = total;
      this.stats.checkedInToday = checkedIn;
      this.stats.upcomingPassengers = upcoming;
      this.stats.flightsToday = flights.size;
    }
  },
  async mounted() {
    // Initialize Bootstrap modal instances once
    if (window.bootstrap && window.bootstrap.Modal) {
      this.ticketDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('ticketDetailsModal'));
      this.processCheckInModalInstance = new window.bootstrap.Modal(document.getElementById('processCheckInModal'));
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

      // Assuming an API endpoint to get all tickets relevant for check-in
      // In a real app, this might be /api/get_tickets_for_checkin/ or similar
      const ticketsResponse = await fetch('/api/get_all_tickets/'); // Fetch all tickets to allow filtering
      const ticketsData = await ticketsResponse.json();
      console.log("Fetched ticketsData:", ticketsData);
      this.tickets = ticketsData.tickets || [];

      this.calculateInitialStats(); // Calculate stats based on fetched data
      this.applyFilters(); // Apply default filter on mount
    } catch (error) {
      console.error("Error fetching data:", error);
      // Fallback for stats if API fails
      this.stats = {
        totalTickets: this.tickets.length,
        checkedInToday: this.tickets.filter(t => t.status === 'checked_in').length,
        upcomingPassengers: this.tickets.filter(t => t.status === 'upcoming').length,
        flightsToday: new Set(this.tickets.map(t => t.flight_number)).size
      };
    }
  }
}
</script>

<style scoped>
/* Base styles */
.check-in-manager-page { /* Changed class name */
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
