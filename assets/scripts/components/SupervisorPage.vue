<template>
  <div class="supervisor-dashboard-page">
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
              <h1 class="display-6 fw-bold text-white mb-2">Supervisor Dashboard</h1>
            </div>
            <p class="text-white-50 mb-0">Full control over system data and operations</p>
          </div>
          <div class="col-md-4 text-md-end">
            <div class="d-flex align-items-center justify-content-md-end">
              <div class="user-info me-3">
                <small class="d-block text-white-50">Welcome back,</small>
                <strong class="text-white">{{ userData.name || 'Supervisor' }}</strong>
              </div>
              <div class="user-avatar">
                <i class="fas fa-user-shield"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-4">
      <!-- Navigation Tabs -->
      <ul class="nav nav-pills mb-4 glass-tabs">
        <li class="nav-item">
          <button class="nav-link" :class="{ active: currentView === 'users' }" @click="currentView = 'users'">
            <i class="fas fa-users me-2"></i>Users
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: currentView === 'flights' }" @click="currentView = 'flights'">
            <i class="fas fa-plane-departure me-2"></i>Flights
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: currentView === 'tickets' }" @click="currentView = 'tickets'">
            <i class="fas fa-ticket-alt me-2"></i>Tickets
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: currentView === 'meals' }" @click="currentView = 'meals'">
            <i class="fas fa-utensils me-2"></i>Meals
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: currentView === 'baggage' }" @click="currentView = 'baggage'">
            <i class="fas fa-suitcase-rolling me-2"></i>Baggage
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: currentView === 'comforts' }" @click="currentView = 'comforts'">
            <i class="fas fa-couch me-2"></i>Comforts
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: currentView === 'airplanes' }" @click="currentView = 'airplanes'">
            <i class="fas fa-plane me-2"></i>Airplanes
          </button>
        </li>
      </ul>

      <!-- Content Area based on currentView -->
      <div class="tab-content">
        <!-- Users Management Section -->
        <div v-if="currentView === 'users'" class="tab-pane fade show active">
          <div class="glass-card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0 text-white"><i class="fas fa-users me-2"></i>Manage Users</h5>
              <button class="btn btn-primary" @click="openCreateEditUserModal()">
                <i class="fas fa-plus me-2"></i>Add New User
              </button>
            </div>
            <div class="card-body p-0">
              <div class="p-4 border-bottom border-secondary">
                <div class="row g-3">
                  <div class="col-md-4">
                    <label class="form-label text-white-50">Search by Name/Email</label>
                    <input type="text" class="form-control glass-input" v-model="userFilters.search" @input="applyUserFilters" placeholder="Search users...">
                  </div>
                  <div class="col-md-4">
                    <label class="form-label text-white-50">Filter by Role</label>
                    <select class="form-select glass-input" v-model="userFilters.role" @change="applyUserFilters">
                      <option value="">All Roles</option>
                      <option value="passenger">Passenger</option>
                      <option value="gate_manager">Gate Manager</option>
                      <option value="checkin_manager">Check-in Manager</option>
                      <option value="supervisor">Supervisor</option>
                    </select>
                  </div>
                  <div class="col-md-4 d-flex align-items-end">
                    <button class="btn btn-outline-light w-100" @click="clearUserFilters">Clear Filters</button>
                  </div>
                </div>
              </div>

              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Last Login</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="paginatedUsers.length === 0">
                      <td colspan="6" class="text-center text-white-50 p-4">No users found.</td>
                    </tr>
                    <tr v-for="user in paginatedUsers" :key="user.id">
                      <td><strong class="text-primary">#{{ user.id }}</strong></td>
                      <td>{{ user.username }}</td>
                      <td>{{ user.email }}</td>
                      <td><span :class="getUserRoleBadgeClass(user.role)">{{ formatStatusForDisplay(user.role) }}</span></td>
                      <td>{{ formatDateTime(user.last_login) }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="viewUserDetails(user)" title="View Details">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button class="btn btn-warning" @click="openCreateEditUserModal(user)" title="Edit User">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger" @click="deleteUser(user)" title="Delete User">
                            <i class="fas fa-trash"></i>
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
                    Showing {{ (userCurrentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(userCurrentPage * itemsPerPage, filteredUsers.length) }}
                    of {{ filteredUsers.length }} entries
                  </span>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: userCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="userCurrentPage = 1" :disabled="userCurrentPage === 1">
                        First
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: userCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="userCurrentPage--" :disabled="userCurrentPage === 1">
                        Previous
                      </button>
                    </li>
                    <li
                      class="page-item"
                      v-for="page in userVisiblePages"
                      :key="page"
                      :class="{ active: page === userCurrentPage }"
                    >
                      <button class="page-link" :class="page === userCurrentPage ? 'bg-primary border-primary' : 'bg-dark border-secondary text-white'" @click="userCurrentPage = page">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: userCurrentPage === userTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="userCurrentPage++" :disabled="userCurrentPage === userTotalPages">
                        Next
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: userCurrentPage === userTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="userCurrentPage = userTotalPages" :disabled="userCurrentPage === userTotalPages">
                        Last
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Flights Management Section -->
        <div v-else-if="currentView === 'flights'" class="tab-pane fade show active">
          <div class="glass-card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0 text-white"><i class="fas fa-plane-departure me-2"></i>Manage Flights</h5>
              <button class="btn btn-primary" @click="openCreateEditFlightModal()">
                <i class="fas fa-plus me-2"></i>Add New Flight
              </button>
            </div>
            <div class="card-body p-0">
              <div class="p-4 border-bottom border-secondary">
                <div class="row g-3">
                  <div class="col-md-4">
                    <label class="form-label text-white-50">Search by Flight/Destination</label>
                    <input type="text" class="form-control glass-input" v-model="flightFilters.search" @input="applyFlightFilters" placeholder="Search flights...">
                  </div>
                  <div class="col-md-4">
                    <label class="form-label text-white-50">Filter by Status</label>
                    <select class="form-select glass-input" v-model="flightFilters.status" @change="applyFlightFilters">
                      <option value="">All Statuses</option>
                      <option value="upcoming">Upcoming</option>
                      <option value="in_air">In Air</option>
                      <option value="arrived">Arrived</option>
                      <option value="canceled">Canceled</option>
                    </select>
                  </div>
                  <div class="col-md-4 d-flex align-items-end">
                    <button class="btn btn-outline-light w-100" @click="clearFlightFilters">Clear Filters</button>
                  </div>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Flight No.</th>
                      <th>Origin</th>
                      <th>Destination</th>
                      <th>Departure</th>
                      <th>Arrival</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="paginatedFlights.length === 0">
                      <td colspan="8" class="text-center text-white-50 p-4">No flights found.</td>
                    </tr>
                    <tr v-for="flight in paginatedFlights" :key="flight.id">
                      <td><strong class="text-primary">#{{ flight.id }}</strong></td>
                      <td>{{ flight.flight_number }}</td>
                      <td>{{ flight.origin }} ({{ flight.origin_code }})</td>
                      <td>{{ flight.destination }} ({{ flight.destination_code }})</td>
                      <td>{{ formatDateTime(flight.departure_time) }}</td>
                      <td>{{ formatDateTime(flight.arrival_time) }}</td>
                      <td><span :class="getFlightStatusBadgeClass(flight.status)">{{ formatStatusForDisplay(flight.status) }}</span></td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="viewFlightDetails(flight)" title="View Details">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button class="btn btn-warning" @click="openCreateEditFlightModal(flight)" title="Edit Flight">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger" @click="deleteFlight(flight)" title="Delete Flight">
                            <i class="fas fa-trash"></i>
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
                    Showing {{ (flightCurrentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(flightCurrentPage * itemsPerPage, filteredFlights.length) }}
                    of {{ filteredFlights.length }} entries
                  </span>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: flightCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="flightCurrentPage = 1" :disabled="flightCurrentPage === 1">
                        First
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: flightCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="flightCurrentPage--" :disabled="flightCurrentPage === 1">
                        Previous
                      </button>
                    </li>
                    <li
                      class="page-item"
                      v-for="page in flightVisiblePages"
                      :key="page"
                      :class="{ active: page === flightCurrentPage }"
                    >
                      <button class="page-link" :class="page === flightCurrentPage ? 'bg-primary border-primary' : 'bg-dark border-secondary text-white'" @click="flightCurrentPage = page">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: flightCurrentPage === flightTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="flightCurrentPage++" :disabled="flightCurrentPage === flightTotalPages">
                        Next
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: flightCurrentPage === flightTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="flightCurrentPage = flightTotalPages" :disabled="flightCurrentPage === flightTotalPages">
                        Last
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Tickets Management Section -->
        <div v-else-if="currentView === 'tickets'" class="tab-pane fade show active">
          <div class="glass-card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0 text-white"><i class="fas fa-ticket-alt me-2"></i>Manage Tickets</h5>
              <button class="btn btn-primary" @click="openCreateEditTicketModal()">
                <i class="fas fa-plus me-2"></i>Add New Ticket
              </button>
            </div>
            <div class="card-body p-0">
              <div class="p-4 border-bottom border-secondary">
                <div class="row g-3">
                  <div class="col-md-4">
                    <label class="form-label text-white-50">Search by Ticket ID/Passenger</label>
                    <input type="text" class="form-control glass-input" v-model="ticketFilters.search" @input="applyTicketFilters" placeholder="Search tickets...">
                  </div>
                  <div class="col-md-4">
                    <label class="form-label text-white-50">Filter by Status</label>
                    <select class="form-select glass-input" v-model="ticketFilters.status" @change="applyTicketFilters">
                      <option value="">All Statuses</option>
                      <option value="upcoming">Upcoming</option>
                      <option value="checked_in">Checked In</option>
                      <option value="boarded">Boarded</option>
                      <option value="used">Used</option>
                      <option value="canceled">Canceled</option>
                      <option value="late">Late</option>
                    </select>
                  </div>
                  <div class="col-md-4 d-flex align-items-end">
                    <button class="btn btn-outline-light w-100" @click="clearTicketFilters">Clear Filters</button>
                  </div>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Booking Ref.</th>
                      <th>Passenger</th>
                      <th>Flight No.</th>
                      <th>Seat</th>
                      <th>Class</th>
                      <th>Status</th>
                      <th>Price</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="paginatedTickets.length === 0">
                      <td colspan="9" class="text-center text-white-50 p-4">No tickets found.</td>
                    </tr>
                    <tr v-for="ticket in paginatedTickets" :key="ticket.id">
                      <td><strong class="text-primary">#{{ ticket.id }}</strong></td>
                      <td>{{ ticket.booking_reference }}</td>
                      <td>{{ ticket.passenger_username }}</td>
                      <td>{{ ticket.flight_number }}</td>
                      <td>{{ ticket.seat_number }}</td>
                      <td>{{ formatStatusForDisplay(ticket.seat_class) }}</td>
                      <td><span :class="getTicketStatusBadgeClass(ticket.status)">{{ formatStatusForDisplay(ticket.status) }}</span></td>
                      <td>${{ ticket.price }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="viewTicketDetails(ticket)" title="View Details">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button class="btn btn-warning" @click="openCreateEditTicketModal(ticket)" title="Edit Ticket">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger" @click="deleteTicket(ticket)" title="Delete Ticket">
                            <i class="fas fa-trash"></i>
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
                    Showing {{ (ticketCurrentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(ticketCurrentPage * itemsPerPage, filteredTickets.length) }}
                    of {{ filteredTickets.length }} entries
                  </span>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: ticketCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="ticketCurrentPage = 1" :disabled="ticketCurrentPage === 1">
                        First
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: ticketCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="ticketCurrentPage--" :disabled="ticketCurrentPage === 1">
                        Previous
                      </button>
                    </li>
                    <li
                      class="page-item"
                      v-for="page in ticketVisiblePages"
                      :key="page"
                      :class="{ active: page === ticketCurrentPage }"
                    >
                      <button class="page-link" :class="page === ticketCurrentPage ? 'bg-primary border-primary' : 'bg-dark border-secondary text-white'" @click="ticketCurrentPage = page">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: ticketCurrentPage === ticketTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="ticketCurrentPage++" :disabled="ticketCurrentPage === ticketTotalPages">
                        Next
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: ticketCurrentPage === ticketTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="ticketCurrentPage = ticketTotalPages" :disabled="ticketCurrentPage === ticketTotalPages">
                        Last
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Meals Management Section -->
        <div v-else-if="currentView === 'meals'" class="tab-pane fade show active">
          <div class="glass-card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0 text-white"><i class="fas fa-utensils me-2"></i>Manage Meals</h5>
              <button class="btn btn-primary" @click="openCreateEditMealModal()">
                <i class="fas fa-plus me-2"></i>Add New Meal
              </button>
            </div>
            <div class="card-body p-0">
              <div class="p-4 border-bottom border-secondary">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label text-white-50">Search by Name/Description</label>
                    <input type="text" class="form-control glass-input" v-model="mealFilters.search" @input="applyMealFilters" placeholder="Search meals...">
                  </div>
                  <div class="col-md-6 d-flex align-items-end">
                    <button class="btn btn-outline-light w-100" @click="clearMealFilters">Clear Filters</button>
                  </div>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Price</th>
                      <th>Description</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="paginatedMeals.length === 0">
                      <td colspan="5" class="text-center text-white-50 p-4">No meals found.</td>
                    </tr>
                    <tr v-for="meal in paginatedMeals" :key="meal.id">
                      <td><strong class="text-primary">#{{ meal.id }}</strong></td>
                      <td>{{ meal.name }}</td>
                      <td>${{ meal.price }}</td>
                      <td>{{ meal.description.substring(0, 50) + (meal.description.length > 50 ? '...' : '') }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="viewMealDetails(meal)" title="View Details">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button class="btn btn-warning" @click="openCreateEditMealModal(meal)" title="Edit Meal">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger" @click="deleteMeal(meal)" title="Delete Meal">
                            <i class="fas fa-trash"></i>
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
                    Showing {{ (mealCurrentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(mealCurrentPage * itemsPerPage, filteredMeals.length) }}
                    of {{ filteredMeals.length }} entries
                  </span>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: mealCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="mealCurrentPage = 1" :disabled="mealCurrentPage === 1">
                        First
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: mealCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="mealCurrentPage--" :disabled="mealCurrentPage === 1">
                        Previous
                      </button>
                    </li>
                    <li
                      class="page-item"
                      v-for="page in mealVisiblePages"
                      :key="page"
                      :class="{ active: page === mealCurrentPage }"
                    >
                      <button class="page-link" :class="page === mealCurrentPage ? 'bg-primary border-primary' : 'bg-dark border-secondary text-white'" @click="mealCurrentPage = page">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: mealCurrentPage === mealTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="mealCurrentPage++" :disabled="mealCurrentPage === mealTotalPages">
                        Next
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: mealCurrentPage === mealTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="mealCurrentPage = mealTotalPages" :disabled="mealCurrentPage === mealTotalPages">
                        Last
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Baggage Management Section -->
        <div v-else-if="currentView === 'baggage'" class="tab-pane fade show active">
          <div class="glass-card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0 text-white"><i class="fas fa-suitcase-rolling me-2"></i>Manage Baggage Options</h5>
              <button class="btn btn-primary" @click="openCreateEditBaggageModal()">
                <i class="fas fa-plus me-2"></i>Add New Baggage Option
              </button>
            </div>
            <div class="card-body p-0">
              <div class="p-4 border-bottom border-secondary">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label text-white-50">Search by Name/Description</label>
                    <input type="text" class="form-control glass-input" v-model="baggageFilters.search" @input="applyBaggageFilters" placeholder="Search baggage options...">
                  </div>
                  <div class="col-md-6 d-flex align-items-end">
                    <button class="btn btn-outline-light w-100" @click="clearBaggageFilters">Clear Filters</button>
                  </div>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Price</th>
                      <th>Weight (kg)</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="paginatedBaggageOptions.length === 0">
                      <td colspan="5" class="text-center text-white-50 p-4">No baggage options found.</td>
                    </tr>
                    <tr v-for="baggage in paginatedBaggageOptions" :key="baggage.id">
                      <td><strong class="text-primary">#{{ baggage.id }}</strong></td>
                      <td>{{ baggage.name }}</td>
                      <td>${{ baggage.price }}</td>
                      <td>{{ baggage.weight }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="viewBaggageDetails(baggage)" title="View Details">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button class="btn btn-warning" @click="openCreateEditBaggageModal(baggage)" title="Edit Baggage">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger" @click="deleteBaggage(baggage)" title="Delete Baggage">
                            <i class="fas fa-trash"></i>
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
                    Showing {{ (baggageCurrentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(baggageCurrentPage * itemsPerPage, filteredBaggageOptions.length) }}
                    of {{ filteredBaggageOptions.length }} entries
                  </span>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: baggageCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="baggageCurrentPage = 1" :disabled="baggageCurrentPage === 1">
                        First
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: baggageCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="baggageCurrentPage--" :disabled="baggageCurrentPage === 1">
                        Previous
                      </button>
                    </li>
                    <li
                      class="page-item"
                      v-for="page in baggageVisiblePages"
                      :key="page"
                      :class="{ active: page === baggageCurrentPage }"
                    >
                      <button class="page-link" :class="page === baggageCurrentPage ? 'bg-primary border-primary' : 'bg-dark border-secondary text-white'" @click="baggageCurrentPage = page">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: baggageCurrentPage === baggageTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="baggageCurrentPage++" :disabled="baggageCurrentPage === baggageTotalPages">
                        Next
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: baggageCurrentPage === baggageTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="baggageCurrentPage = baggageTotalPages" :disabled="baggageCurrentPage === baggageTotalPages">
                        Last
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Comforts Management Section -->
        <div v-else-if="currentView === 'comforts'" class="tab-pane fade show active">
          <div class="glass-card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0 text-white"><i class="fas fa-couch me-2"></i>Manage Comfort Options</h5>
              <button class="btn btn-primary" @click="openCreateEditComfortModal()">
                <i class="fas fa-plus me-2"></i>Add New Comfort Option
              </button>
            </div>
            <div class="card-body p-0">
              <div class="p-4 border-bottom border-secondary">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label text-white-50">Search by Name/Description</label>
                    <input type="text" class="form-control glass-input" v-model="comfortFilters.search" @input="applyComfortFilters" placeholder="Search comfort options...">
                  </div>
                  <div class="col-md-6 d-flex align-items-end">
                    <button class="btn btn-outline-light w-100" @click="clearComfortFilters">Clear Filters</button>
                  </div>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Price</th>
                      <th>Description</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="paginatedComfortOptions.length === 0">
                      <td colspan="5" class="text-center text-white-50 p-4">No comfort options found.</td>
                    </tr>
                    <tr v-for="comfort in paginatedComfortOptions" :key="comfort.id">
                      <td><strong class="text-primary">#{{ comfort.id }}</strong></td>
                      <td>{{ comfort.name }}</td>
                      <td>${{ comfort.price }}</td>
                      <td>{{ comfort.description.substring(0, 50) + (comfort.description.length > 50 ? '...' : '') }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="viewComfortDetails(comfort)" title="View Details">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button class="btn btn-warning" @click="openCreateEditComfortModal(comfort)" title="Edit Comfort">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger" @click="deleteComfort(comfort)" title="Delete Comfort">
                            <i class="fas fa-trash"></i>
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
                    Showing {{ (comfortCurrentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(comfortCurrentPage * itemsPerPage, filteredComfortOptions.length) }}
                    of {{ filteredComfortOptions.length }} entries
                  </span>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: comfortCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="comfortCurrentPage = 1" :disabled="comfortCurrentPage === 1">
                        First
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: comfortCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="comfortCurrentPage--" :disabled="comfortCurrentPage === 1">
                        Previous
                      </button>
                    </li>
                    <li
                      class="page-item"
                      v-for="page in comfortVisiblePages"
                      :key="page"
                      :class="{ active: page === comfortCurrentPage }"
                    >
                      <button class="page-link" :class="page === comfortCurrentPage ? 'bg-primary border-primary' : 'bg-dark border-secondary text-white'" @click="comfortCurrentPage = page">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: comfortCurrentPage === comfortTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="comfortCurrentPage++" :disabled="comfortCurrentPage === comfortTotalPages">
                        Next
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: comfortCurrentPage === comfortTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="comfortCurrentPage = comfortTotalPages" :disabled="comfortCurrentPage === comfortTotalPages">
                        Last
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Airplanes Management Section -->
        <div v-else-if="currentView === 'airplanes'" class="tab-pane fade show active">
          <div class="glass-card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0 text-white"><i class="fas fa-plane me-2"></i>Manage Airplanes</h5>
              <button class="btn btn-primary" @click="openCreateEditAirplaneModal()">
                <i class="fas fa-plus me-2"></i>Add New Airplane
              </button>
            </div>
            <div class="card-body p-0">
              <div class="p-4 border-bottom border-secondary">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label text-white-50">Search by Name</label>
                    <input type="text" class="form-control glass-input" v-model="airplaneFilters.search" @input="applyAirplaneFilters" placeholder="Search airplanes...">
                  </div>
                  <div class="col-md-6 d-flex align-items-end">
                    <button class="btn btn-outline-light w-100" @click="clearAirplaneFilters">Clear Filters</button>
                  </div>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-dark mb-0 table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Capacity</th>
                      <th>Economy</th>
                      <th>Business</th>
                      <th>First Class</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="paginatedAirplanes.length === 0">
                      <td colspan="7" class="text-center text-white-50 p-4">No airplanes found.</td>
                    </tr>
                    <tr v-for="airplane in paginatedAirplanes" :key="airplane.id">
                      <td><strong class="text-primary">#{{ airplane.id }}</strong></td>
                      <td>{{ airplane.name }}</td>
                      <td>{{ airplane.seat_capacity }}</td>
                      <td>{{ airplane.economy_seats }}</td>
                      <td>{{ airplane.business_seats }}</td>
                      <td>{{ airplane.first_class_seats }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="viewAirplaneDetails(airplane)" title="View Details">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button class="btn btn-warning" @click="openCreateEditAirplaneModal(airplane)" title="Edit Airplane">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger" @click="deleteAirplane(airplane)" title="Delete Airplane">
                            <i class="fas fa-trash"></i>
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
                    Showing {{ (airplaneCurrentPage - 1) * itemsPerPage + 1 }} to
                    {{ Math.min(airplaneCurrentPage * itemsPerPage, filteredAirplanes.length) }}
                    of {{ filteredAirplanes.length }} entries
                  </span>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: airplaneCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="airplaneCurrentPage = 1" :disabled="airplaneCurrentPage === 1">
                        First
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: airplaneCurrentPage === 1 }">
                      <button class="page-link bg-dark border-secondary text-white" @click="airplaneCurrentPage--" :disabled="airplaneCurrentPage === 1">
                        Previous
                      </button>
                    </li>
                    <li
                      class="page-item"
                      v-for="page in airplaneVisiblePages"
                      :key="page"
                      :class="{ active: page === airplaneCurrentPage }"
                    >
                      <button class="page-link" :class="page === airplaneCurrentPage ? 'bg-primary border-primary' : 'bg-dark border-secondary text-white'" @click="airplaneCurrentPage = page">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: airplaneCurrentPage === airplaneTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="airplaneCurrentPage++" :disabled="airplaneCurrentPage === airplaneTotalPages">
                        Next
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: airplaneCurrentPage === airplaneTotalPages }">
                      <button class="page-link bg-dark border-secondary text-white" @click="airplaneCurrentPage = airplaneTotalPages" :disabled="airplaneCurrentPage === airplaneTotalPages">
                        Last
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div class="modal fade" id="userDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">User Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedUser">
            <div class="row">
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-primary">General Information</h6>
                <table class="table table-dark table-borderless">
                  <tr>
                    <td class="fw-semibold">ID:</td>
                    <td><strong class="text-primary">#{{ selectedUser.id }}</strong></td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Username:</td>
                    <td>{{ selectedUser.username }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Email:</td>
                    <td>{{ selectedUser.email }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">First Name:</td>
                    <td>{{ selectedUser.first_name || 'N/A' }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Last Name:</td>
                    <td>{{ selectedUser.last_name || 'N/A' }}</td>
                  </tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Account Information</h6>
                <table class="table table-dark table-borderless">
                  <tr>
                    <td class="fw-semibold">Role:</td>
                    <td><span :class="getUserRoleBadgeClass(selectedUser.role)">{{ formatStatusForDisplay(selectedUser.role) }}</span></td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Active:</td>
                    <td>
                      <i class="fas" :class="selectedUser.is_active ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'"></i>
                      {{ selectedUser.is_active ? 'Yes' : 'No' }}
                    </td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Staff:</td>
                    <td>
                      <i class="fas" :class="selectedUser.is_staff ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'"></i>
                      {{ selectedUser.is_staff ? 'Yes' : 'No' }}
                    </td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Superuser:</td>
                    <td>
                      <i class="fas" :class="selectedUser.is_superuser ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'"></i>
                      {{ selectedUser.is_superuser ? 'Yes' : 'No' }}
                    </td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Last Login:</td>
                    <td>{{ formatDateTime(selectedUser.last_login) }}</td>
                  </tr>
                  <tr>
                    <td class="fw-semibold">Date Joined:</td>
                    <td>{{ formatDateTime(selectedUser.date_joined) }}</td>
                  </tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-warning" @click="openCreateEditUserModal(selectedUser)" data-bs-dismiss="modal">
              <i class="fas fa-edit me-2"></i>Edit User
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <div class="modal fade" id="createEditUserModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">{{ editUserForm.id ? 'Edit User' : 'Create New User' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveUser">
              <div class="mb-3">
                <label for="username" class="form-label fw-semibold">Username <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="username" v-model="editUserForm.username" required>
              </div>
              <div class="mb-3">
                <label for="email" class="form-label fw-semibold">Email <span class="text-danger">*</span></label>
                <input type="email" class="form-control glass-input" id="email" v-model="editUserForm.email" required>
              </div>
              <div class="mb-3">
                <label for="first_name" class="form-label fw-semibold">First Name</label>
                <input type="text" class="form-control glass-input" id="first_name" v-model="editUserForm.first_name">
              </div>
              <div class="mb-3">
                <label for="last_name" class="form-label fw-semibold">Last Name</label>
                <input type="text" class="form-control glass-input" id="last_name" v-model="editUserForm.last_name">
              </div>
              <div class="mb-3">
                <label for="role" class="form-label fw-semibold">Role <span class="text-danger">*</span></label>
                <select class="form-select glass-input" id="role" v-model="editUserForm.role" required>
                  <option value="passenger">Passenger</option>
                  <option value="gate_manager">Gate Manager</option>
                  <option value="checkin_manager">Check-in Manager</option>
                  <option value="supervisor">Supervisor</option>
                </select>
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="is_active" v-model="editUserForm.is_active">
                <label class="form-check-label" for="is_active">Is Active</label>
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="is_staff" v-model="editUserForm.is_staff">
                <label class="form-check-label" for="is_staff">Is Staff</label>
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="is_superuser" v-model="editUserForm.is_superuser">
                <label class="form-check-label" for="is_superuser">Is Superuser</label>
              </div>
              <div class="mb-4" v-if="!editUserForm.id">
                <label for="password" class="form-label fw-semibold">Password <span class="text-danger">*</span></label>
                <input type="password" class="form-control glass-input" id="password" v-model="editUserForm.password" required>
                <div class="form-text text-white-50">Password is required for new users. For existing users, password cannot be changed here.</div>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-save me-2"></i>Save User
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Flight Details Modal (Placeholder) -->
    <div class="modal fade" id="flightDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Flight Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedFlight">
            <div class="row">
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-primary">Flight Information</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">ID:</td><td><strong class="text-primary">#{{ selectedFlight.id }}</strong></td></tr>
                  <tr><td class="fw-semibold">Flight Number:</td><td>{{ selectedFlight.flight_number }}</td></tr>
                  <tr><td class="fw-semibold">Origin:</td><td>{{ selectedFlight.origin }} ({{ selectedFlight.origin_code }})</td></tr>
                  <tr><td class="fw-semibold">Destination:</td><td>{{ selectedFlight.destination }} ({{ selectedFlight.destination_code }})</td></tr>
                  <tr><td class="fw-semibold">Departure:</td><td>{{ formatDateTime(selectedFlight.departure_time) }}</td></tr>
                  <tr><td class="fw-semibold">Arrival:</td><td>{{ formatDateTime(selectedFlight.arrival_time) }}</td></tr>
                  <tr><td class="fw-semibold">Status:</td><td><span :class="getFlightStatusBadgeClass(selectedFlight.status)">{{ formatStatusForDisplay(selectedFlight.status) }}</span></td></tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Pricing & Airplane</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">Base Price:</td><td>${{ selectedFlight.base_price }}</td></tr>
                  <tr><td class="fw-semibold">Airplane:</td><td>{{ selectedFlight.airplane_name || 'N/A' }}</td></tr>
                  <tr><td class="fw-semibold">Capacity:</td><td>{{ selectedFlight.airplane_seat_capacity || 'N/A' }}</td></tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-warning" @click="openCreateEditFlightModal(selectedFlight)" data-bs-dismiss="modal">
              <i class="fas fa-edit me-2"></i>Edit Flight
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Flight Modal (Placeholder) -->
    <div class="modal fade" id="createEditFlightModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">{{ editFlightForm.id ? 'Edit Flight' : 'Create New Flight' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveFlight">
              <div class="mb-3">
                <label for="flight_number" class="form-label fw-semibold">Flight Number <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="flight_number" v-model="editFlightForm.flight_number" required>
              </div>
              <div class="mb-3">
                <label for="origin" class="form-label fw-semibold">Origin <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="origin" v-model="editFlightForm.origin" required>
              </div>
              <div class="mb-3">
                <label for="origin_code" class="form-label fw-semibold">Origin Code</label>
                <input type="text" class="form-control glass-input" id="origin_code" v-model="editFlightForm.origin_code">
              </div>
              <div class="mb-3">
                <label for="destination" class="form-label fw-semibold">Destination <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="destination" v-model="editFlightForm.destination" required>
              </div>
              <div class="mb-3">
                <label for="destination_code" class="form-label fw-semibold">Destination Code</label>
                <input type="text" class="form-control glass-input" id="destination_code" v-model="editFlightForm.destination_code">
              </div>
              <div class="mb-3">
                <label for="departure_time" class="form-label fw-semibold">Departure Time <span class="text-danger">*</span></label>
                <input type="datetime-local" class="form-control glass-input" id="departure_time" v-model="editFlightForm.departure_time" required>
              </div>
              <div class="mb-3">
                <label for="arrival_time" class="form-label fw-semibold">Arrival Time <span class="text-danger">*</span></label>
                <input type="datetime-local" class="form-control glass-input" id="arrival_time" v-model="editFlightForm.arrival_time" required>
              </div>
              <div class="mb-3">
                <label for="base_price" class="form-label fw-semibold">Base Price <span class="text-danger">*</span></label>
                <input type="number" step="0.01" class="form-control glass-input" id="base_price" v-model.number="editFlightForm.base_price" required>
              </div>
              <div class="mb-3">
                <label for="airplane" class="form-label fw-semibold">Airplane</label>
                <select class="form-select glass-input" id="airplane" v-model="editFlightForm.airplane">
                  <option :value="null">None</option>
                  <option v-for="airplane in airplanes" :key="airplane.id" :value="airplane.id">{{ airplane.name }} ({{ airplane.seat_capacity }} seats)</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="flight_status" class="form-label fw-semibold">Status <span class="text-danger">*</span></label>
                <select class="form-select glass-input" id="flight_status" v-model="editFlightForm.status" required>
                  <option value="upcoming">Upcoming</option>
                  <option value="in_air">In Air</option>
                  <option value="arrived">Arrived</option>
                  <option value="canceled">Canceled</option>
                </select>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-save me-2"></i>Save Flight
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Ticket Details Modal (Placeholder) -->
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
                <h6 class="fw-bold mb-3 text-primary">Ticket Information</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">ID:</td><td><strong class="text-primary">#{{ selectedTicket.id }}</strong></td></tr>
                  <tr><td class="fw-semibold">Booking Ref:</td><td>{{ selectedTicket.booking_reference }}</td></tr>
                  <tr><td class="fw-semibold">Seat:</td><td>{{ selectedTicket.seat_number }} ({{ formatStatusForDisplay(selectedTicket.seat_class) }})</td></tr>
                  <tr><td class="fw-semibold">Gate:</td><td>{{ selectedTicket.gate || 'N/A' }}</td></tr>
                  <tr><td class="fw-semibold">Price:</td><td>${{ selectedTicket.price }}</td></tr>
                  <tr><td class="fw-semibold">Status:</td><td><span :class="getTicketStatusBadgeClass(selectedTicket.status)">{{ formatStatusForDisplay(selectedTicket.status) }}</span></td></tr>
                  <tr><td class="fw-semibold">Checked In:</td><td><i class="fas" :class="selectedTicket.is_checked_in ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'"></i> {{ selectedTicket.is_checked_in ? 'Yes' : 'No' }}</td></tr>
                  <tr><td class="fw-semibold">Boarded:</td><td><i class="fas" :class="selectedTicket.is_boarded ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'"></i> {{ selectedTicket.is_boarded ? 'Yes' : 'No' }}</td></tr>
                  <tr><td class="fw-semibold">Created At:</td><td>{{ formatDateTime(selectedTicket.created_at) }}</td></tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Passenger & Flight</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">Passenger:</td><td>{{ selectedTicket.passenger_username }} ({{ selectedTicket.passenger_email }})</td></tr>
                  <tr><td class="fw-semibold">Flight:</td><td>{{ selectedTicket.flight_number }} ({{ selectedTicket.flight_destination }})</td></tr>
                  <tr><td class="fw-semibold">Departure:</td><td>{{ formatDateTime(selectedTicket.flight_departure_time) }}</td></tr>
                  <tr><td class="fw-semibold">Meals:</td><td>{{ selectedTicket.meals_names && selectedTicket.meals_names.length > 0 ? selectedTicket.meals_names.join(', ') : 'None' }}</td></tr>
                  <tr><td class="fw-semibold">Baggage:</td><td>{{ selectedTicket.baggage_names && selectedTicket.baggage_names.length > 0 ? selectedTicket.baggage_names.join(', ') : 'None' }}</td></tr>
                  <tr><td class="fw-semibold">Comforts:</td><td>{{ selectedTicket.comforts_names && selectedTicket.comforts_names.length > 0 ? selectedTicket.comforts_names.join(', ') : 'None' }}</td></tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-warning" @click="openCreateEditTicketModal(selectedTicket)" data-bs-dismiss="modal">
              <i class="fas fa-edit me-2"></i>Edit Ticket
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Ticket Modal (Placeholder) -->
    <div class="modal fade" id="createEditTicketModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">{{ editTicketForm.id ? 'Edit Ticket' : 'Create New Ticket' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveTicket">
              <div class="mb-3">
                <label for="passenger" class="form-label fw-semibold">Passenger <span class="text-danger">*</span></label>
                <select class="form-select glass-input" id="passenger" v-model="editTicketForm.passenger" required>
                  <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }} ({{ user.email }})</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="flight" class="form-label fw-semibold">Flight <span class="text-danger">*</span></label>
                <select class="form-select glass-input" id="flight" v-model="editTicketForm.flight" required>
                  <option v-for="flight in flights" :key="flight.id" :value="flight.id">{{ flight.flight_number }} ({{ flight.origin }} - {{ flight.destination }})</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="seat_number" class="form-label fw-semibold">Seat Number <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="seat_number" v-model="editTicketForm.seat_number" required>
              </div>
              <div class="mb-3">
                <label for="seat_class" class="form-label fw-semibold">Seat Class <span class="text-danger">*</span></label>
                <select class="form-select glass-input" id="seat_class" v-model="editTicketForm.seat_class" required>
                  <option value="economy">Economy</option>
                  <option value="business">Business</option>
                  <option value="first">First</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="gate" class="form-label fw-semibold">Gate</label>
                <input type="number" class="form-control glass-input" id="gate" v-model.number="editTicketForm.gate">
              </div>
              <div class="mb-3">
                <label for="price" class="form-label fw-semibold">Price <span class="text-danger">*</span></label>
                <input type="number" step="0.01" class="form-control glass-input" id="price" v-model.number="editTicketForm.price" required>
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="is_checked_in" v-model="editTicketForm.is_checked_in">
                <label class="form-check-label" for="is_checked_in">Is Checked In</label>
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="is_boarded" v-model="editTicketForm.is_boarded">
                <label class="form-check-label" for="is_boarded">Is Boarded</label>
              </div>
              <div class="mb-3">
                <label for="ticket_status" class="form-label fw-semibold">Status <span class="text-danger">*</span></label>
                <select class="form-select glass-input" id="ticket_status" v-model="editTicketForm.status" required>
                  <option value="upcoming">Upcoming</option>
                  <option value="checked_in">Checked In</option>
                  <option value="boarded">Boarded</option>
                  <option value="used">Used</option>
                  <option value="canceled">Canceled</option>
                  <option value="late">Late</option>
                </select>
              </div>
              <!-- Multi-select for Meals, Baggage, Comforts -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Meals</label>
                <select class="form-select glass-input" multiple v-model="editTicketForm.meals">
                  <option v-for="meal in meals" :key="meal.id" :value="meal.id">{{ meal.name }} (${{ meal.price }})</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Baggage Options</label>
                <select class="form-select glass-input" multiple v-model="editTicketForm.baggage">
                  <option v-for="baggage in baggageOptions" :key="baggage.id" :value="baggage.id">{{ baggage.name }} (${{ baggage.price }})</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Comfort Options</label>
                <select class="form-select glass-input" multiple v-model="editTicketForm.comforts">
                  <option v-for="comfort in comfortOptions" :key="comfort.id" :value="comfort.id">{{ comfort.name }} (${{ comfort.price }})</option>
                </select>
              </div>

              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-save me-2"></i>Save Ticket
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Meal Details Modal (Placeholder) -->
    <div class="modal fade" id="mealDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Meal Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedMeal">
            <div class="row">
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-primary">Meal Information</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">ID:</td><td><strong class="text-primary">#{{ selectedMeal.id }}</strong></td></tr>
                  <tr><td class="fw-semibold">Name:</td><td>{{ selectedMeal.name }}</td></tr>
                  <tr><td class="fw-semibold">Price:</td><td>${{ selectedMeal.price }}</td></tr>
                  <tr><td class="fw-semibold">Stripe Price ID:</td><td>{{ selectedMeal.stripe_price_id }}</td></tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Details</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">Description:</td><td>{{ selectedMeal.description }}</td></tr>
                  <tr><td class="fw-semibold">Dietary Options:</td><td>{{ selectedMeal.dietary_options_names && selectedMeal.dietary_options_names.length > 0 ? selectedMeal.dietary_options_names.join(', ') : 'None' }}</td></tr>
                  <tr><td class="fw-semibold">Image:</td><td><img :src="selectedMeal.image_url" alt="Meal Image" class="img-fluid rounded" style="max-height: 100px;"></td></tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-warning" @click="openCreateEditMealModal(selectedMeal)" data-bs-dismiss="modal">
              <i class="fas fa-edit me-2"></i>Edit Meal
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Meal Modal (Placeholder) -->
    <div class="modal fade" id="createEditMealModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">{{ editMealForm.id ? 'Edit Meal' : 'Create New Meal' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveMeal">
              <div class="mb-3">
                <label for="meal_name" class="form-label fw-semibold">Name <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="meal_name" v-model="editMealForm.name" required>
              </div>
              <div class="mb-3">
                <label for="meal_description" class="form-label fw-semibold">Description <span class="text-danger">*</span></label>
                <textarea class="form-control glass-input" id="meal_description" v-model="editMealForm.description" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label for="meal_price" class="form-label fw-semibold">Price <span class="text-danger">*</span></label>
                <input type="number" step="0.01" class="form-control glass-input" id="meal_price" v-model.number="editMealForm.price" required>
              </div>
              <div class="mb-3">
                <label for="meal_image_url" class="form-label fw-semibold">Image URL</label>
                <input type="url" class="form-control glass-input" id="meal_image_url" v-model="editMealForm.image_url">
              </div>
              <div class="mb-3">
                <label for="meal_stripe_price_id" class="form-label fw-semibold">Stripe Price ID <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="meal_stripe_price_id" v-model="editMealForm.stripe_price_id" required>
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Dietary Options</label>
                <select class="form-select glass-input" multiple v-model="editMealForm.dietary_options">
                  <option v-for="option in dietaryOptions" :key="option.id" :value="option.id">{{ option.name }}</option>
                </select>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-save me-2"></i>Save Meal
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Baggage Details Modal (Placeholder) -->
    <div class="modal fade" id="baggageDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Baggage Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedBaggage">
            <div class="row">
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-primary">Baggage Information</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">ID:</td><td><strong class="text-primary">#{{ selectedBaggage.id }}</strong></td></tr>
                  <tr><td class="fw-semibold">Name:</td><td>{{ selectedBaggage.name }}</td></tr>
                  <tr><td class="fw-semibold">Price:</td><td>${{ selectedBaggage.price }}</td></tr>
                  <tr><td class="fw-semibold">Weight:</td><td>{{ selectedBaggage.weight }} kg</td></tr>
                  <tr><td class="fw-semibold">Stripe Price ID:</td><td>{{ selectedBaggage.stripe_price_id }}</td></tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Description</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">Description:</td><td>{{ selectedBaggage.description }}</td></tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-warning" @click="openCreateEditBaggageModal(selectedBaggage)" data-bs-dismiss="modal">
              <i class="fas fa-edit me-2"></i>Edit Baggage
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Baggage Modal (Placeholder) -->
    <div class="modal fade" id="createEditBaggageModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">{{ editBaggageForm.id ? 'Edit Baggage Option' : 'Create New Baggage Option' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveBaggage">
              <div class="mb-3">
                <label for="baggage_name" class="form-label fw-semibold">Name <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="baggage_name" v-model="editBaggageForm.name" required>
              </div>
              <div class="mb-3">
                <label for="baggage_description" class="form-label fw-semibold">Description <span class="text-danger">*</span></label>
                <textarea class="form-control glass-input" id="baggage_description" v-model="editBaggageForm.description" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label for="baggage_price" class="form-label fw-semibold">Price <span class="text-danger">*</span></label>
                <input type="number" step="0.01" class="form-control glass-input" id="baggage_price" v-model.number="editBaggageForm.price" required>
              </div>
              <div class="mb-3">
                <label for="baggage_weight" class="form-label fw-semibold">Weight (kg) <span class="text-danger">*</span></label>
                <input type="number" step="0.01" class="form-control glass-input" id="baggage_weight" v-model.number="editBaggageForm.weight" required>
              </div>
              <div class="mb-3">
                <label for="baggage_stripe_price_id" class="form-label fw-semibold">Stripe Price ID <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="baggage_stripe_price_id" v-model="editBaggageForm.stripe_price_id" required>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-save me-2"></i>Save Baggage Option
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Comfort Details Modal (Placeholder) -->
    <div class="modal fade" id="comfortDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Comfort Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedComfort">
            <div class="row">
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-primary">Comfort Information</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">ID:</td><td><strong class="text-primary">#{{ selectedComfort.id }}</strong></td></tr>
                  <tr><td class="fw-semibold">Name:</td><td>{{ selectedComfort.name }}</td></tr>
                  <tr><td class="fw-semibold">Price:</td><td>${{ selectedComfort.price }}</td></tr>
                  <tr><td class="fw-semibold">Stripe Price ID:</td><td>{{ selectedComfort.stripe_price_id }}</td></tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Description</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">Description:</td><td>{{ selectedComfort.description }}</td></tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-warning" @click="openCreateEditComfortModal(selectedComfort)" data-bs-dismiss="modal">
              <i class="fas fa-edit me-2"></i>Edit Comfort
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Comfort Modal (Placeholder) -->
    <div class="modal fade" id="createEditComfortModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">{{ editComfortForm.id ? 'Edit Comfort Option' : 'Create New Comfort Option' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveComfort">
              <div class="mb-3">
                <label for="comfort_name" class="form-label fw-semibold">Name <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="comfort_name" v-model="editComfortForm.name" required>
              </div>
              <div class="mb-3">
                <label for="comfort_description" class="form-label fw-semibold">Description <span class="text-danger">*</span></label>
                <textarea class="form-control glass-input" id="comfort_description" v-model="editComfortForm.description" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label for="comfort_price" class="form-label fw-semibold">Price <span class="text-danger">*</span></label>
                <input type="number" step="0.01" class="form-control glass-input" id="comfort_price" v-model.number="editComfortForm.price" required>
              </div>
              <div class="mb-3">
                <label for="comfort_stripe_price_id" class="form-label fw-semibold">Stripe Price ID <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="comfort_stripe_price_id" v-model="editComfortForm.stripe_price_id" required>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-save me-2"></i>Save Comfort Option
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Airplane Details Modal (Placeholder) -->
    <div class="modal fade" id="airplaneDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Airplane Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedAirplane">
            <div class="row">
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-primary">Airplane Information</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">ID:</td><td><strong class="text-primary">#{{ selectedAirplane.id }}</strong></td></tr>
                  <tr><td class="fw-semibold">Name:</td><td>{{ selectedAirplane.name }}</td></tr>
                  <tr><td class="fw-semibold">Total Capacity:</td><td>{{ selectedAirplane.seat_capacity }}</td></tr>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="fw-bold mb-3 text-success">Seat Distribution</h6>
                <table class="table table-dark table-borderless">
                  <tr><td class="fw-semibold">Economy Seats:</td><td>{{ selectedAirplane.economy_seats }}</td></tr>
                  <tr><td class="fw-semibold">Business Seats:</td><td>{{ selectedAirplane.business_seats }}</td></tr>
                  <tr><td class="fw-semibold">First Class Seats:</td><td>{{ selectedAirplane.first_class_seats }}</td></tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-warning" @click="openCreateEditAirplaneModal(selectedAirplane)" data-bs-dismiss="modal">
              <i class="fas fa-edit me-2"></i>Edit Airplane
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Airplane Modal (Placeholder) -->
    <div class="modal fade" id="createEditAirplaneModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">{{ editAirplaneForm.id ? 'Edit Airplane' : 'Create New Airplane' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveAirplane">
              <div class="mb-3">
                <label for="airplane_name" class="form-label fw-semibold">Name <span class="text-danger">*</span></label>
                <input type="text" class="form-control glass-input" id="airplane_name" v-model="editAirplaneForm.name" required>
              </div>
              <div class="mb-3">
                <label for="seat_capacity" class="form-label fw-semibold">Total Seat Capacity <span class="text-danger">*</span></label>
                <input type="number" class="form-control glass-input" id="seat_capacity" v-model.number="editAirplaneForm.seat_capacity" required min="1">
              </div>
              <div class="mb-3">
                <label for="economy_seats" class="form-label fw-semibold">Economy Seats <span class="text-danger">*</span></label>
                <input type="number" class="form-control glass-input" id="economy_seats" v-model.number="editAirplaneForm.economy_seats" required min="0">
              </div>
              <div class="mb-3">
                <label for="business_seats" class="form-label fw-semibold">Business Seats <span class="text-danger">*</span></label>
                <input type="number" class="form-control glass-input" id="business_seats" v-model.number="editAirplaneForm.business_seats" required min="0">
              </div>
              <div class="mb-3">
                <label for="first_class_seats" class="form-label fw-semibold">First Class Seats <span class="text-danger">*</span></label>
                <input type="number" class="form-control glass-input" id="first_class_seats" v-model.number="editAirplaneForm.first_class_seats" required min="0">
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-save me-2"></i>Save Airplane
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'SupervisorDashboard',
  data() {
    return {
      userData: {
        name: 'Supervisor',
        email: '',
        id: '',
        role: 'supervisor'
      },
      currentView: 'users', // Default view
      itemsPerPage: 10,

      // User Management Data
      users: [],
      filteredUsers: [],
      selectedUser: null,
      userFilters: {
        search: '',
        role: ''
      },
      userCurrentPage: 1,
      editUserForm: {
        id: null,
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: 'passenger',
        is_active: true,
        is_staff: false,
        is_superuser: false,
        password: '', // Only for creation, not sent for update
      },

      // Flight Management Data
      flights: [],
      filteredFlights: [],
      selectedFlight: null,
      flightFilters: {
        search: '',
        status: ''
      },
      flightCurrentPage: 1,
      editFlightForm: {
        id: null,
        flight_number: '',
        origin: '',
        destination: '',
        origin_code: '',
        destination_code: '',
        departure_time: '',
        arrival_time: '',
        base_price: 0.00,
        airplane: null, // ID of the airplane
        status: 'upcoming',
      },

      // Ticket Management Data
      tickets: [],
      filteredTickets: [],
      selectedTicket: null,
      ticketFilters: {
        search: '',
        status: ''
      },
      ticketCurrentPage: 1,
      editTicketForm: {
        id: null,
        passenger: null, // ID of the passenger
        flight: null, // ID of the flight
        seat_number: '',
        seat_class: 'economy',
        gate: null,
        meals: [], // Array of meal IDs
        baggage: [], // Array of baggage IDs
        comforts: [], // Array of comfort IDs
        price: 0.00,
        is_checked_in: false,
        is_boarded: false,
        status: 'upcoming',
      },

      // Meal Management Data
      meals: [],
      filteredMeals: [],
      selectedMeal: null,
      mealFilters: {
        search: ''
      },
      mealCurrentPage: 1,
      editMealForm: {
        id: null,
        name: '',
        description: '',
        price: 0.00,
        image_url: '',
        dietary_options: [], // Array of DietaryOption IDs
        stripe_price_id: '',
      },
      dietaryOptions: [], // To populate dropdown for meals

      // Baggage Management Data
      baggageOptions: [], // Renamed to avoid conflict with 'baggage' in Ticket model
      filteredBaggageOptions: [],
      selectedBaggage: null,
      baggageFilters: {
        search: ''
      },
      baggageCurrentPage: 1,
      editBaggageForm: {
        id: null,
        name: '',
        description: '',
        price: 0.00,
        weight: 0.00,
        stripe_price_id: '',
      },

      // Comfort Management Data
      comfortOptions: [],
      filteredComfortOptions: [],
      selectedComfort: null,
      comfortFilters: {
        search: ''
      },
      comfortCurrentPage: 1,
      editComfortForm: {
        id: null,
        name: '',
        description: '',
        price: 0.00,
        stripe_price_id: '',
      },

      // Airplane Management Data
      airplanes: [],
      filteredAirplanes: [],
      selectedAirplane: null,
      airplaneFilters: {
        search: ''
      },
      airplaneCurrentPage: 1,
      editAirplaneForm: {
        id: null,
        name: '',
        seat_capacity: 0,
        economy_seats: 0,
        business_seats: 0,
        first_class_seats: 0,
      },

      // Modal Instances
      userDetailsModalInstance: null,
      createEditUserModalInstance: null,
      flightDetailsModalInstance: null,
      createEditFlightModalInstance: null,
      ticketDetailsModalInstance: null,
      createEditTicketModalInstance: null,
      mealDetailsModalInstance: null,
      createEditMealModalInstance: null,
      baggageDetailsModalInstance: null,
      createEditBaggageModalInstance: null,
      comfortDetailsModalInstance: null,
      createEditComfortModalInstance: null,
      airplaneDetailsModalInstance: null,
      createEditAirplaneModalInstance: null,
    };
  },
  computed: {
    // User Management Computed Properties
    paginatedUsers() {
      const start = (this.userCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredUsers.slice(start, end);
    },
    userTotalPages() {
      return Math.ceil(this.filteredUsers.length / this.itemsPerPage);
    },
    userVisiblePages() {
      const pages = [];
      const start = Math.max(1, this.userCurrentPage - 2);
      const end = Math.min(this.userTotalPages, this.userCurrentPage + 2);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    // Flight Management Computed Properties
    paginatedFlights() {
      const start = (this.flightCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredFlights.slice(start, end);
    },
    flightTotalPages() {
      return Math.ceil(this.filteredFlights.length / this.itemsPerPage);
    },
    flightVisiblePages() {
      const pages = [];
      const start = Math.max(1, this.flightCurrentPage - 2);
      const end = Math.min(this.flightTotalPages, this.flightCurrentPage + 2);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    // Ticket Management Computed Properties
    paginatedTickets() {
      const start = (this.ticketCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTickets.slice(start, end);
    },
    ticketTotalPages() {
      return Math.ceil(this.filteredTickets.length / this.itemsPerPage);
    },
    ticketVisiblePages() {
      const pages = [];
      const start = Math.max(1, this.ticketCurrentPage - 2);
      const end = Math.min(this.ticketTotalPages, this.ticketCurrentPage + 2);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    // Meal Management Computed Properties
    paginatedMeals() {
      const start = (this.mealCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredMeals.slice(start, end);
    },
    mealTotalPages() {
      return Math.ceil(this.filteredMeals.length / this.itemsPerPage);
    },
    mealVisiblePages() {
      const pages = [];
      const start = Math.max(1, this.mealCurrentPage - 2);
      const end = Math.min(this.mealTotalPages, this.mealCurrentPage + 2);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    // Baggage Management Computed Properties
    paginatedBaggageOptions() {
      const start = (this.baggageCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredBaggageOptions.slice(start, end);
    },
    baggageTotalPages() {
      return Math.ceil(this.filteredBaggageOptions.length / this.itemsPerPage);
    },
    baggageVisiblePages() {
      const pages = [];
      const start = Math.max(1, this.baggageCurrentPage - 2);
      const end = Math.min(this.baggageTotalPages, this.baggageCurrentPage + 2);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    // Comfort Management Computed Properties
    paginatedComfortOptions() {
      const start = (this.comfortCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredComfortOptions.slice(start, end);
    },
    comfortTotalPages() {
      return Math.ceil(this.filteredComfortOptions.length / this.itemsPerPage);
    },
    comfortVisiblePages() {
      const pages = [];
      const start = Math.max(1, this.comfortCurrentPage - 2);
      const end = Math.min(this.comfortTotalPages, this.comfortCurrentPage + 2);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    // Airplane Management Computed Properties
    paginatedAirplanes() {
      const start = (this.airplaneCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredAirplanes.slice(start, end);
    },
    airplaneTotalPages() {
      return Math.ceil(this.filteredAirplanes.length / this.itemsPerPage);
    },
    airplaneVisiblePages() {
      const pages = [];
      const start = Math.max(1, this.airplaneCurrentPage - 2);
      const end = Math.min(this.airplaneTotalPages, this.airplaneCurrentPage + 2);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },
  },
  watch: {
    'currentView': 'fetchDataForCurrentView', // Watch for tab changes
    'userFilters.search': 'applyUserFilters',
    'userFilters.role': 'applyUserFilters',
    'flightFilters.search': 'applyFlightFilters',
    'flightFilters.status': 'applyFlightFilters',
    'ticketFilters.search': 'applyTicketFilters',
    'ticketFilters.status': 'applyTicketFilters',
    'mealFilters.search': 'applyMealFilters',
    'baggageFilters.search': 'applyBaggageFilters',
    'comfortFilters.search': 'applyComfortFilters',
    'airplaneFilters.search': 'applyAirplaneFilters',
  },
  methods: {
    // --- General Utility Methods ---
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
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        // Handle 'None' or invalid date strings by returning N/A
        if (dateString === null) return 'N/A';
        console.error('Error formatting datetime:', error);
        return 'Invalid Date';
      }
    },
    formatStatusForDisplay(status) {
      if (!status) return 'N/A';
      return status.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
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
    goToHomePage() {
      window.location.href = '/';
    },

    // --- Data Fetching for Current View ---
    fetchDataForCurrentView() {
      switch (this.currentView) {
        case 'users':
          this.fetchUsers();
          break;
        case 'flights':
          this.fetchFlights();
          this.fetchAirplanes(); // Flights need airplane data for dropdown
          break;
        case 'tickets':
          this.fetchTickets();
          this.fetchUsers(); // Tickets need user data for dropdown
          this.fetchFlights(); // Tickets need flight data for dropdown
          this.fetchMeals(); // Tickets need meals for dropdown
          this.fetchBaggageOptions(); // Tickets need baggage for dropdown
          this.fetchComfortOptions(); // Tickets need comforts for dropdown
          break;
        case 'meals':
          this.fetchMeals();
          // Assuming DietaryOption is a separate model, fetch it too
          this.fetchDietaryOptions();
          break;
        case 'baggage':
          this.fetchBaggageOptions();
          break;
        case 'comforts':
          this.fetchComfortOptions();
          break;
        case 'airplanes':
          this.fetchAirplanes();
          break;
        default:
          break;
      }
    },

    // --- User Management Methods ---
    getUserRoleBadgeClass(role) {
      const classes = {
        'passenger': 'badge bg-info',
        'gate_manager': 'badge bg-warning text-dark',
        'checkin_manager': 'badge bg-success',
        'supervisor': 'badge bg-primary',
      };
      return classes[role] || 'badge bg-secondary';
    },
    async fetchUsers() {
      try {
        const response = await fetch('/api/users/'); // Adjust API endpoint as needed
        if (!response.ok) throw new Error("Failed to fetch users");
        this.users = await response.json();
        this.applyUserFilters();
      } catch (error) {
        console.error("Error fetching users:", error);
        this.showErrorMessage("Could not load users.");
      }
    },
    applyUserFilters() {
      this.filteredUsers = this.users.filter(user => {
        const matchesSearch = !this.userFilters.search ||
          (user.username && user.username.toLowerCase().includes(this.userFilters.search.toLowerCase())) ||
          (user.email && user.email.toLowerCase().includes(this.userFilters.search.toLowerCase()));

        const matchesRole = !this.userFilters.role || user.role === this.userFilters.role;

        return matchesSearch && matchesRole;
      });
      this.userCurrentPage = 1;
    },
    clearUserFilters() {
      this.userFilters.search = '';
      this.userFilters.role = '';
      this.applyUserFilters();
    },
    viewUserDetails(user) {
      this.selectedUser = { ...user }; // Create a copy to prevent direct modification
      if (this.userDetailsModalInstance) {
        this.userDetailsModalInstance.show();
      }
    },
    openCreateEditUserModal(user = null) {
      // Reset form
      this.editUserForm = {
        id: null,
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: 'passenger',
        is_active: true,
        is_staff: false,
        is_superuser: false,
        password: '', // Only for creation
      };

      if (user) {
        // Populate form for editing
        this.editUserForm = { ...user };
        // Password is not editable directly via this form for security reasons
        // It should be handled via a separate password reset/change mechanism if needed.
        delete this.editUserForm.password;
      }

      if (this.createEditUserModalInstance) {
        this.createEditUserModalInstance.show();
      }
    },
    async saveUser() {
      const isEditing = !!this.editUserForm.id;
      const url = isEditing ? `/api/users/${this.editUserForm.id}/` : '/api/users/';
      const method = isEditing ? 'PUT' : 'POST';

      // Prepare payload
      const payload = { ...this.editUserForm };
      if (isEditing) {
        // Remove password from payload if editing, as it shouldn't be sent back
        delete payload.password;
      } else {
        // For new user, password is required
        if (!payload.password) {
          this.showErrorMessage('Password is required for new users.');
          return;
        }
      }

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to save user: " + (errorData.detail || errorData.username || errorData.email || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`User ${isEditing ? 'updated' : 'created'} successfully!`);
        if (this.createEditUserModalInstance) {
          this.createEditUserModalInstance.hide();
        }
        this.fetchUsers(); // Refresh data
      } catch (error) {
        console.error("Error saving user:", error);
        this.showErrorMessage("An error occurred while saving user. Please try again.");
      }
    },
    async deleteUser(user) {
      if (!confirm(`Are you sure you want to delete user "${user.username}"?`)) {
        return;
      }

      try {
        const response = await fetch(`/api/users/${user.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to delete user: " + (errorData.detail || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`User "${user.username}" deleted successfully.`);
        this.fetchUsers(); // Refresh data
      } catch (error) {
        console.error("Error deleting user:", error);
        this.showErrorMessage("An error occurred while deleting user. Please try again.");
      }
    },

    // --- Flight Management Methods ---
    getFlightStatusBadgeClass(status) {
      const classes = {
        'upcoming': 'badge bg-info',
        'in_air': 'badge bg-primary',
        'arrived': 'badge bg-success',
        'canceled': 'badge bg-danger',
      };
      return classes[status] || 'badge bg-secondary';
    },
    async fetchFlights() {
      try {
        const response = await fetch('/api/flights/'); // Adjust API endpoint as needed
        if (!response.ok) throw new Error("Failed to fetch flights");
        this.flights = await response.json();
        this.applyFlightFilters();
      } catch (error) {
        console.error("Error fetching flights:", error);
        this.showErrorMessage("Could not load flights.");
      }
    },
    applyFlightFilters() {
      this.filteredFlights = this.flights.filter(flight => {
        const matchesSearch = !this.flightFilters.search ||
          (flight.flight_number && flight.flight_number.toLowerCase().includes(this.flightFilters.search.toLowerCase())) ||
          (flight.origin && flight.origin.toLowerCase().includes(this.flightFilters.search.toLowerCase())) ||
          (flight.destination && flight.destination.toLowerCase().includes(this.flightFilters.search.toLowerCase()));

        const matchesStatus = !this.flightFilters.status || flight.status === this.flightFilters.status;

        return matchesSearch && matchesStatus;
      });
      this.flightCurrentPage = 1;
    },
    clearFlightFilters() {
      this.flightFilters.search = '';
      this.flightFilters.status = '';
      this.applyFlightFilters();
    },
    viewFlightDetails(flight) {
      this.selectedFlight = { ...flight };
      if (this.flightDetailsModalInstance) {
        this.flightDetailsModalInstance.show();
      }
    },
    openCreateEditFlightModal(flight = null) {
      this.editFlightForm = {
        id: null,
        flight_number: '',
        origin: '',
        destination: '',
        origin_code: '',
        destination_code: '',
        departure_time: '',
        arrival_time: '',
        base_price: 0.00,
        airplane: null,
        status: 'upcoming',
      };
      if (flight) {
        this.editFlightForm = {
          ...flight,
          // Format dates for datetime-local input
          departure_time: flight.departure_time ? new Date(flight.departure_time).toISOString().slice(0, 16) : '',
          arrival_time: flight.arrival_time ? new Date(flight.arrival_time).toISOString().slice(0, 16) : '',
          airplane: flight.airplane_id || null // Assuming API returns airplane_id
        };
      }
      if (this.createEditFlightModalInstance) {
        this.createEditFlightModalInstance.show();
      }
    },
    async saveFlight() {
      const isEditing = !!this.editFlightForm.id;
      const url = isEditing ? `/api/flights/${this.editFlightForm.id}/` : '/api/flights/';
      const method = isEditing ? 'PUT' : 'POST';

      const payload = { ...this.editFlightForm };
      // Ensure price is a number
      payload.base_price = parseFloat(payload.base_price);

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to save flight: " + (errorData.detail || errorData.flight_number || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`Flight ${isEditing ? 'updated' : 'created'} successfully!`);
        if (this.createEditFlightModalInstance) {
          this.createEditFlightModalInstance.hide();
        }
        this.fetchFlights(); // Refresh data
      } catch (error) {
        console.error("Error saving flight:", error);
        this.showErrorMessage("An error occurred while saving flight. Please try again.");
      }
    },
    async deleteFlight(flight) {
      if (!confirm(`Are you sure you want to delete flight "${flight.flight_number}"?`)) {
        return;
      }
      try {
        const response = await fetch(`/api/flights/${flight.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to delete flight: " + (errorData.detail || "Unknown error"));
          return;
        }
        this.showSuccessMessage(`Flight "${flight.flight_number}" deleted successfully.`);
        this.fetchFlights();
      } catch (error) {
        console.error("Error deleting flight:", error);
        this.showErrorMessage("An error occurred while deleting flight. Please try again.");
      }
    },

    // --- Ticket Management Methods ---
    getTicketStatusBadgeClass(status) {
      const classes = {
        'upcoming': 'badge bg-warning text-dark',
        'checked_in': 'badge bg-success',
        'boarded': 'badge bg-primary',
        'used': 'badge bg-secondary',
        'canceled': 'badge bg-danger',
        'late': 'badge bg-danger',
      };
      return classes[status] || 'badge bg-secondary';
    },
    async fetchTickets() {
      try {
        const response = await fetch('/api/tickets/'); // Adjust API endpoint as needed
        if (!response.ok) throw new Error("Failed to fetch tickets");
        this.tickets = await response.json();
        this.applyTicketFilters();
      } catch (error) {
        console.error("Error fetching tickets:", error);
        this.showErrorMessage("Could not load tickets.");
      }
    },
    applyTicketFilters() {
      this.filteredTickets = this.tickets.filter(ticket => {
        const matchesSearch = !this.ticketFilters.search ||
          (ticket.booking_reference && ticket.booking_reference.toLowerCase().includes(this.ticketFilters.search.toLowerCase())) ||
          (ticket.passenger_username && ticket.passenger_username.toLowerCase().includes(this.ticketFilters.search.toLowerCase())) ||
          (ticket.flight_number && ticket.flight_number.toLowerCase().includes(this.ticketFilters.search.toLowerCase()));

        const matchesStatus = !this.ticketFilters.status || ticket.status === this.ticketFilters.status;

        return matchesSearch && matchesStatus;
      });
      this.ticketCurrentPage = 1;
    },
    clearTicketFilters() {
      this.ticketFilters.search = '';
      this.ticketFilters.status = '';
      this.applyTicketFilters();
    },
    viewTicketDetails(ticket) {
      this.selectedTicket = { ...ticket };
      if (this.ticketDetailsModalInstance) {
        this.ticketDetailsModalInstance.show();
      }
    },
    openCreateEditTicketModal(ticket = null) {
      this.editTicketForm = {
        id: null,
        passenger: null,
        flight: null,
        seat_number: '',
        seat_class: 'economy',
        gate: null,
        meals: [],
        baggage: [],
        comforts: [],
        price: 0.00,
        is_checked_in: false,
        is_boarded: false,
        status: 'upcoming',
      };
      if (ticket) {
        this.editTicketForm = {
          ...ticket,
          passenger: ticket.passenger_id, // Assuming API returns passenger_id
          flight: ticket.flight_id, // Assuming API returns flight_id
          meals: ticket.meals_ids || [], // Assuming API returns meals_ids
          baggage: ticket.baggage_ids || [], // Assuming API returns baggage_ids
          comforts: ticket.comforts_ids || [], // Assuming API returns comforts_ids
        };
      }
      if (this.createEditTicketModalInstance) {
        this.createEditTicketModalInstance.show();
      }
    },
    async saveTicket() {
      const isEditing = !!this.editTicketForm.id;
      const url = isEditing ? `/api/tickets/${this.editTicketForm.id}/` : '/api/tickets/';
      const method = isEditing ? 'PUT' : 'POST';

      const payload = { ...this.editTicketForm };
      payload.price = parseFloat(payload.price);

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to save ticket: " + (errorData.detail || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`Ticket ${isEditing ? 'updated' : 'created'} successfully!`);
        if (this.createEditTicketModalInstance) {
          this.createEditTicketModalInstance.hide();
        }
        this.fetchTickets();
      } catch (error) {
        console.error("Error saving ticket:", error);
        this.showErrorMessage("An error occurred while saving ticket. Please try again.");
      }
    },
    async deleteTicket(ticket) {
      if (!confirm(`Are you sure you want to delete ticket "${ticket.booking_reference}"?`)) {
        return;
      }
      try {
        const response = await fetch(`/api/tickets/${ticket.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to delete ticket: " + (errorData.detail || "Unknown error"));
          return;
        }
        this.showSuccessMessage(`Ticket "${ticket.booking_reference}" deleted successfully.`);
        this.fetchTickets();
      } catch (error) {
        console.error("Error deleting ticket:", error);
        this.showErrorMessage("An error occurred while deleting ticket. Please try again.");
      }
    },

    // --- Meal Management Methods ---
    async fetchMeals() {
      try {
        const response = await fetch('/api/meals/');
        if (!response.ok) throw new Error("Failed to fetch meals");
        this.meals = await response.json();
        this.applyMealFilters();
      } catch (error) {
        console.error("Error fetching meals:", error);
        this.showErrorMessage("Could not load meals.");
      }
    },
    async fetchDietaryOptions() {
      try {
        const response = await fetch('/api/dietary_options/'); // Assuming this endpoint exists
        if (!response.ok) throw new Error("Failed to fetch dietary options");
        this.dietaryOptions = await response.json();
      } catch (error) {
        console.error("Error fetching dietary options:", error);
        this.showErrorMessage("Could not load dietary options.");
      }
    },
    applyMealFilters() {
      this.filteredMeals = this.meals.filter(meal => {
        const matchesSearch = !this.mealFilters.search ||
          (meal.name && meal.name.toLowerCase().includes(this.mealFilters.search.toLowerCase())) ||
          (meal.description && meal.description.toLowerCase().includes(this.mealFilters.search.toLowerCase()));
        return matchesSearch;
      });
      this.mealCurrentPage = 1;
    },
    clearMealFilters() {
      this.mealFilters.search = '';
      this.applyMealFilters();
    },
    viewMealDetails(meal) {
      this.selectedMeal = { ...meal };
      if (this.mealDetailsModalInstance) {
        this.mealDetailsModalInstance.show();
      }
    },
    openCreateEditMealModal(meal = null) {
      this.editMealForm = {
        id: null,
        name: '',
        description: '',
        price: 0.00,
        image_url: '',
        dietary_options: [],
        stripe_price_id: '',
      };
      if (meal) {
        this.editMealForm = {
          ...meal,
          dietary_options: meal.dietary_options_ids || [] // Assuming API returns dietary_options_ids
        };
      }
      if (this.createEditMealModalInstance) {
        this.createEditMealModalInstance.show();
      }
    },
    async saveMeal() {
      const isEditing = !!this.editMealForm.id;
      const url = isEditing ? `/api/meals/${this.editMealForm.id}/` : '/api/meals/';
      const method = isEditing ? 'PUT' : 'POST';

      const payload = { ...this.editMealForm };
      payload.price = parseFloat(payload.price);

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to save meal: " + (errorData.detail || errorData.name || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`Meal ${isEditing ? 'updated' : 'created'} successfully!`);
        if (this.createEditMealModalInstance) {
          this.createEditMealModalInstance.hide();
        }
        this.fetchMeals();
      } catch (error) {
        console.error("Error saving meal:", error);
        this.showErrorMessage("An error occurred while saving meal. Please try again.");
      }
    },
    async deleteMeal(meal) {
      if (!confirm(`Are you sure you want to delete meal "${meal.name}"?`)) {
        return;
      }
      try {
        const response = await fetch(`/api/meals/${meal.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to delete meal: " + (errorData.detail || "Unknown error"));
          return;
        }
        this.showSuccessMessage(`Meal "${meal.name}" deleted successfully.`);
        this.fetchMeals();
      } catch (error) {
        console.error("Error deleting meal:", error);
        this.showErrorMessage("An error occurred while deleting meal. Please try again.");
      }
    },

    // --- Baggage Management Methods ---
    async fetchBaggageOptions() {
      try {
        const response = await fetch('/api/baggage/');
        if (!response.ok) throw new Error("Failed to fetch baggage options");
        this.baggageOptions = await response.json();
        this.applyBaggageFilters();
      } catch (error) {
        console.error("Error fetching baggage options:", error);
        this.showErrorMessage("Could not load baggage options.");
      }
    },
    applyBaggageFilters() {
      this.filteredBaggageOptions = this.baggageOptions.filter(baggage => {
        const matchesSearch = !this.baggageFilters.search ||
          (baggage.name && baggage.name.toLowerCase().includes(this.baggageFilters.search.toLowerCase())) ||
          (baggage.description && baggage.description.toLowerCase().includes(this.baggageFilters.search.toLowerCase()));
        return matchesSearch;
      });
      this.baggageCurrentPage = 1;
    },
    clearBaggageFilters() {
      this.baggageFilters.search = '';
      this.applyBaggageFilters();
    },
    viewBaggageDetails(baggage) {
      this.selectedBaggage = { ...baggage };
      if (this.baggageDetailsModalInstance) {
        this.baggageDetailsModalInstance.show();
      }
    },
    openCreateEditBaggageModal(baggage = null) {
      this.editBaggageForm = {
        id: null,
        name: '',
        description: '',
        price: 0.00,
        weight: 0.00,
        stripe_price_id: '',
      };
      if (baggage) {
        this.editBaggageForm = { ...baggage };
      }
      if (this.createEditBaggageModalInstance) {
        this.createEditBaggageModalInstance.show();
      }
    },
    async saveBaggage() {
      const isEditing = !!this.editBaggageForm.id;
      const url = isEditing ? `/api/baggage/${this.editBaggageForm.id}/` : '/api/baggage/';
      const method = isEditing ? 'PUT' : 'POST';

      const payload = { ...this.editBaggageForm };
      payload.price = parseFloat(payload.price);
      payload.weight = parseFloat(payload.weight);

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to save baggage option: " + (errorData.detail || errorData.name || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`Baggage option ${isEditing ? 'updated' : 'created'} successfully!`);
        if (this.createEditBaggageModalInstance) {
          this.createEditBaggageModalInstance.hide();
        }
        this.fetchBaggageOptions();
      } catch (error) {
        console.error("Error saving baggage option:", error);
        this.showErrorMessage("An error occurred while saving baggage option. Please try again.");
      }
    },
    async deleteBaggage(baggage) {
      if (!confirm(`Are you sure you want to delete baggage option "${baggage.name}"?`)) {
        return;
      }
      try {
        const response = await fetch(`/api/baggage/${baggage.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to delete baggage option: " + (errorData.detail || "Unknown error"));
          return;
        }
        this.showSuccessMessage(`Baggage option "${baggage.name}" deleted successfully.`);
        this.fetchBaggageOptions();
      } catch (error) {
        console.error("Error deleting baggage option:", error);
        this.showErrorMessage("An error occurred while deleting baggage option. Please try again.");
      }
    },

    // --- Comfort Management Methods ---
    async fetchComfortOptions() {
      try {
        const response = await fetch('/api/comforts/');
        if (!response.ok) throw new Error("Failed to fetch comfort options");
        this.comfortOptions = await response.json();
        this.applyComfortFilters();
      } catch (error) {
        console.error("Error fetching comfort options:", error);
        this.showErrorMessage("Could not load comfort options.");
      }
    },
    applyComfortFilters() {
      this.filteredComfortOptions = this.comfortOptions.filter(comfort => {
        const matchesSearch = !this.comfortFilters.search ||
          (comfort.name && comfort.name.toLowerCase().includes(this.comfortFilters.search.toLowerCase())) ||
          (comfort.description && comfort.description.toLowerCase().includes(this.comfortFilters.search.toLowerCase()));
        return matchesSearch;
      });
      this.comfortCurrentPage = 1;
    },
    clearComfortFilters() {
      this.comfortFilters.search = '';
      this.applyComfortFilters();
    },
    viewComfortDetails(comfort) {
      this.selectedComfort = { ...comfort };
      if (this.comfortDetailsModalInstance) {
        this.comfortDetailsModalInstance.show();
      }
    },
    openCreateEditComfortModal(comfort = null) {
      this.editComfortForm = {
        id: null,
        name: '',
        description: '',
        price: 0.00,
        stripe_price_id: '',
      };
      if (comfort) {
        this.editComfortForm = { ...comfort };
      }
      if (this.createEditComfortModalInstance) {
        this.createEditComfortModalInstance.show();
      }
    },
    async saveComfort() {
      const isEditing = !!this.editComfortForm.id;
      const url = isEditing ? `/api/comforts/${this.editComfortForm.id}/` : '/api/comforts/';
      const method = isEditing ? 'PUT' : 'POST';

      const payload = { ...this.editComfortForm };
      payload.price = parseFloat(payload.price);

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to save comfort option: " + (errorData.detail || errorData.name || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`Comfort option ${isEditing ? 'updated' : 'created'} successfully!`);
        if (this.createEditComfortModalInstance) {
          this.createEditComfortModalInstance.hide();
        }
        this.fetchComfortOptions();
      } catch (error) {
        console.error("Error saving comfort option:", error);
        this.showErrorMessage("An error occurred while saving comfort option. Please try again.");
      }
    },
    async deleteComfort(comfort) {
      if (!confirm(`Are you sure you want to delete comfort option "${comfort.name}"?`)) {
        return;
      }
      try {
        const response = await fetch(`/api/comforts/${comfort.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to delete comfort option: " + (errorData.detail || "Unknown error"));
          return;
        }
        this.showSuccessMessage(`Comfort option "${comfort.name}" deleted successfully.`);
        this.fetchComfortOptions();
      } catch (error) {
        console.error("Error deleting comfort option:", error);
        this.showErrorMessage("An error occurred while deleting comfort option. Please try again.");
      }
    },

    // --- Airplane Management Methods ---
    async fetchAirplanes() {
      try {
        const response = await fetch('/api/airplanes/');
        if (!response.ok) throw new Error("Failed to fetch airplanes");
        this.airplanes = await response.json();
        this.applyAirplaneFilters();
      } catch (error) {
        console.error("Error fetching airplanes:", error);
        this.showErrorMessage("Could not load airplanes.");
      }
    },
    applyAirplaneFilters() {
      this.filteredAirplanes = this.airplanes.filter(airplane => {
        const matchesSearch = !this.airplaneFilters.search ||
          (airplane.name && airplane.name.toLowerCase().includes(this.airplaneFilters.search.toLowerCase()));
        return matchesSearch;
      });
      this.airplaneCurrentPage = 1;
    },
    clearAirplaneFilters() {
      this.airplaneFilters.search = '';
      this.applyAirplaneFilters();
    },
    viewAirplaneDetails(airplane) {
      this.selectedAirplane = { ...airplane };
      if (this.airplaneDetailsModalInstance) {
        this.airplaneDetailsModalInstance.show();
      }
    },
    openCreateEditAirplaneModal(airplane = null) {
      this.editAirplaneForm = {
        id: null,
        name: '',
        seat_capacity: 0,
        economy_seats: 0,
        business_seats: 0,
        first_class_seats: 0,
      };
      if (airplane) {
        this.editAirplaneForm = { ...airplane };
      }
      if (this.createEditAirplaneModalInstance) {
        this.createEditAirplaneModalInstance.show();
      }
    },
    async saveAirplane() {
      const isEditing = !!this.editAirplaneForm.id;
      const url = isEditing ? `/api/airplanes/${this.editAirplaneForm.id}/` : '/api/airplanes/';
      const method = isEditing ? 'PUT' : 'POST';

      const payload = { ...this.editAirplaneForm };
      // Ensure seat counts are numbers
      payload.seat_capacity = parseInt(payload.seat_capacity);
      payload.economy_seats = parseInt(payload.economy_seats);
      payload.business_seats = parseInt(payload.business_seats);
      payload.first_class_seats = parseInt(payload.first_class_seats);

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to save airplane: " + (errorData.detail || errorData.name || "Unknown error"));
          return;
        }

        this.showSuccessMessage(`Airplane ${isEditing ? 'updated' : 'created'} successfully!`);
        if (this.createEditAirplaneModalInstance) {
          this.createEditAirplaneModalInstance.hide();
        }
        this.fetchAirplanes();
      } catch (error) {
        console.error("Error saving airplane:", error);
        this.showErrorMessage("An error occurred while saving airplane. Please try again.");
      }
    },
    async deleteAirplane(airplane) {
      if (!confirm(`Are you sure you want to delete airplane "${airplane.name}"?`)) {
        return;
      }
      try {
        const response = await fetch(`/api/airplanes/${airplane.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error:", errorData);
          this.showErrorMessage("Failed to delete airplane: " + (errorData.detail || "Unknown error"));
          return;
        }
        this.showSuccessMessage(`Airplane "${airplane.name}" deleted successfully.`);
        this.fetchAirplanes();
      } catch (error) {
        console.error("Error deleting airplane:", error);
        this.showErrorMessage("An error occurred while deleting airplane. Please try again.");
      }
    },
  },
  async mounted() {
    // Initialize Bootstrap modal instances
    if (window.bootstrap && window.bootstrap.Modal) {
      this.userDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('userDetailsModal'));
      this.createEditUserModalInstance = new window.bootstrap.Modal(document.getElementById('createEditUserModal'));
      this.flightDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('flightDetailsModal'));
      this.createEditFlightModalInstance = new window.bootstrap.Modal(document.getElementById('createEditFlightModal'));
      this.ticketDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('ticketDetailsModal'));
      this.createEditTicketModalInstance = new window.bootstrap.Modal(document.getElementById('createEditTicketModal'));
      this.mealDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('mealDetailsModal'));
      this.createEditMealModalInstance = new window.bootstrap.Modal(document.getElementById('createEditMealModal'));
      this.baggageDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('baggageDetailsModal'));
      this.createEditBaggageModalInstance = new window.bootstrap.Modal(document.getElementById('createEditBaggageModal'));
      this.comfortDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('comfortDetailsModal'));
      this.createEditComfortModalInstance = new window.bootstrap.Modal(document.getElementById('createEditComfortModal'));
      this.airplaneDetailsModalInstance = new window.bootstrap.Modal(document.getElementById('airplaneDetailsModal'));
      this.createEditAirplaneModalInstance = new window.bootstrap.Modal(document.getElementById('createEditAirplaneModal'));
    } else {
      console.warn('Bootstrap Modal not found. Modals may not function correctly.');
    }

    try {
      const userResponse = await fetch('/api/current_user/');
      const userData = await userResponse.json();
      // Assume supervisor is always authenticated if accessing this page
      this.userData = {
        name: userData.user.first_name || userData.user.username || 'Supervisor',
        email: userData.user.email,
        id: userData.user.id,
        role: userData.user.role,
      };

      // Fetch initial data for the default view (Users)
      this.fetchDataForCurrentView();
    } catch (error) {
      console.error("Error fetching current user data:", error);
      this.showErrorMessage("Failed to load user profile. Some features may be limited.");
      // Fallback for user data if API fails
      this.userData.name = 'Guest Supervisor';
    }
  }
}
</script>

<style scoped>
/* Base styles */
.supervisor-dashboard-page {
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
.user-avatar i { /* For font-awesome icon */
  font-size: 1.4rem;
}

/* Navigation Tabs */
.glass-tabs .nav-link {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(5px);
  margin-right: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
  padding: 0.75rem 1.25rem;
}

.glass-tabs .nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.glass-tabs .nav-link.active {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-tertiary) 100%) !important;
  border-color: var(--color-primary) !important;
  color: white;
  box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);
}

/* Glass Card Effect (for content sections) */
.glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
}

/* Glass Input Styling */
.glass-input {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  backdrop-filter: blur(10px);
  border-radius: 12px;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.15) !important;
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 0.2rem rgba(108, 99, 255, 0.25) !important;
  color: white !important;
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.5) !important;
}

.form-select option {
  background-color: var(--color-dark);
  color: var(--color-light);
}

/* Card Header */
.card-header {
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}

/* Table Styling */
.table-dark {
  --bs-table-bg: transparent;
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

.table-hover tbody tr:hover {
  background-color: rgba(108, 99, 255, 0.15) !important;
  transition: background-color 0.2s ease;
}

/* Button Styling */
.btn-primary {
  background: linear-gradient(45deg, var(--color-primary), var(--color-tertiary));
  border: none;
  color: white;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(108, 99, 255, 0.4);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-weight: 600;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(108, 99, 255, 0.6);
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 8px;
  padding: 0.5rem 1rem;
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
  padding: 0.5rem 1rem;
  font-weight: 600;
}

.btn-success:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(86, 171, 47, 0.4);
}

.btn-warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 600;
  color: #333; /* Darker text for better contrast */
}
.btn-warning:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(240, 147, 251, 0.4);
}

.btn-danger {
  background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 600;
}
.btn-danger:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(255, 65, 108, 0.4);
}

/* Button group specific styles for rounded corners */
.btn-group-sm .btn {
  padding: 0.375rem 0.5rem;
  border-radius: 6px;
}
.btn-group-sm .btn:not(:first-child) {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
}
.btn-group-sm .btn:not(:last-child) {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
}

/* Modal Styling */
.modal-content {
  background: var(--color-dark) !important;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header, .modal-footer {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1);
}

.btn-close-white {
  filter: invert(1);
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
  .glass-tabs .nav-link {
    margin-bottom: 0.5rem;
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
