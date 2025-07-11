<template>
<div class="tickets-app">
  <!-- Main background that spans all sections -->
  <div class="main-background">
    <div class="stars-container">
      <div class="stars stars-1"></div>
      <div class="stars stars-2"></div>
      <div class="stars stars-3"></div>
    </div>

    <div class="animated-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
      <div class="shape shape-4"></div>
      <div class="shape shape-5"></div>
    </div>
  </div>

  <!-- User Profile Button -->
  <div v-if="isAuthenticated" class="user-profile-container">
    <button @click.stop="showUserProfile" class="user-profile-button">
      <span class="user-avatar">{{ userInitials }}</span>
    </button>

    <!-- Profile Dropdown Menu -->
    <div v-if="isProfileMenuOpen" class="profile-dropdown">
      <div class="profile-header">
        <span class="profile-name">{{ userData.name }}</span>
        <span class="profile-email">{{ userData.email }}</span>
      </div>
      <div class="profile-menu-items">
        <a href="/" class="profile-menu-item" disabled>Home</a>
        <a href="/bookings" class="profile-menu-item active">My Tickets</a>
        <button @click="logout" class="profile-menu-item logout-button">Logout</button>
      </div>
    </div>
  </div>

  <!-- Auth Required Message -->
  <div v-if="showAuthRequiredMessage" class="auth-required-message">
    <div class="auth-required-content">
      <button @click="closeAuthRequiredMessage" class="close-button">&times;</button>
      <h3>Authentication Required</h3>
      <p>Please login or register to view your tickets.</p>
      <div class="auth-buttons">
        <button @click="openLoginModal" class="btn-login">Login</button>
        <button @click="openRegisterModal" class="btn-register">Register</button>
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="container py-5 z-index-2 position-relative min-vh-100">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <!-- Header -->
        <div class="text-center mb-5">
          <h1 class="display-5 fw-bold text-gradient-alt">My Tickets</h1>
          <p class="text-white opacity-75">View and manage your flight tickets</p>
        </div>

        <!-- Tickets Filter -->
        <div class="card glass-card border-0 rounded-4 mb-5">
          <div class="card-body p-4">
            <div class="row g-3 align-items-center">
              <div class="col-md-4">
                <label for="filter-status" class="form-label fw-medium text-white">Filter by Status</label>
                <select id="filter-status" v-model="filterStatus" class="form-select form-control-lg bg-transparent text-white">
                  <option value="all">All Tickets</option>
                  <option value="upcoming">Upcoming</option>
                  <option value="past">Past</option>
                  <option value="canceled">Canceled</option>
                </select>
              </div>
              <div class="col-md-4">
                <label for="sort-by" class="form-label fw-medium text-white">Sort by</label>
                <select id="sort-by" v-model="sortBy" class="form-select form-control-lg bg-transparent text-white">
                  <option value="date-asc">Date (Oldest First)</option>
                  <option value="date-desc">Date (Newest First)</option>
                  <option value="destination">Destination</option>
                </select>
              </div>
              <div class="col-md-4">
                <label for="search" class="form-label fw-medium text-white">Search</label>
                <div class="input-group input-group-glow">
                  <span class="input-group-text bg-transparent border-end-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-search text-primary" viewBox="0 0 16 16">
                      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                    </svg>
                  </span>
                  <input type="text" id="search" v-model="searchQuery" class="form-control form-control-lg bg-transparent border-start-0 text-white" placeholder="Search destination...">
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-5">
          <div class="spinner-container">
            <div class="spinner"></div>
          </div>
          <p class="text-white mt-3">Loading your tickets...</p>
        </div>

        <!-- No Tickets State -->
        <div v-else-if="filteredTickets.length === 0" class="card glass-card border-0 rounded-4 text-center py-5">
          <div class="card-body">
            <div class="empty-state-icon mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" class="bi bi-ticket-perforated text-primary" viewBox="0 0 16 16">
                <path d="M4 4.85v.9h1v-.9H4Zm7 0v.9h1v-.9h-1Zm-7 1.8v.9h1v-.9H4Zm7 0v.9h1v-.9h-1Zm-7 1.8v.9h1v-.9H4Zm7 0v.9h1v-.9h-1Zm-7 1.8v.9h1v-.9H4Zm7 0v.9h1v-.9h-1Z"/>
                <path d="M1.5 3A1.5 1.5 0 0 0 0 4.5V6a.5.5 0 0 0 .5.5 1.5 1.5 0 1 1 0 3 .5.5 0 0 0-.5.5v1.5A1.5 1.5 0 0 0 1.5 13h13a1.5 1.5 0 0 0 1.5-1.5V10a.5.5 0 0 0-.5-.5 1.5 1.5 0 0 1 0-3A.5.5 0 0 0 16 6V4.5A1.5 1.5 0 0 0 14.5 3h-13ZM1 4.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 .5.5v1.05a2.5 2.5 0 0 0 0 4.9v1.05a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5v-1.05a2.5 2.5 0 0 0 0-4.9V4.5Z"/>
              </svg>
            </div>
            <h3 class="fs-4 fw-semibold text-white mb-3">No tickets found</h3>
            <p class="text-white opacity-75 mb-4">You don't have any tickets matching your current filters.</p>
            <button @click="resetFilters" class="btn btn-glow px-4 py-2 rounded-pill">
              <span class="fw-medium">Reset Filters</span>
            </button>
            <a href="/" class="btn btn-outline-light px-4 py-2 rounded-pill ms-2">
              <span class="fw-medium">Book a Flight</span>
            </a>
          </div>
        </div>

        <!-- Tickets List -->
        <div v-else>
          <div v-for="ticket in filteredTickets" :key="ticket.id" class="ticket-card mb-4">
            <div class="card glass-card border-0 rounded-4 overflow-hidden">
              <div class="card-body p-0">
                <!-- Ticket Status Badge -->
                <div :class="`ticket-status-badge ${ticket.status}`">
                  {{ formatStatus(ticket.status) }}
                </div>

                <!-- Ticket Header -->
                <div class="ticket-header p-4">
                  <div class="row align-items-center">
                    <div class="col-md-8">
                      <div class="d-flex align-items-center">
                        <div class="airline-logo me-3">
                          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-airplane text-primary" viewBox="0 0 16 16">
                            <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
                          </svg>
                        </div>
                        <div>
                          <h3 class="fs-4 fw-semibold text-white mb-1">Flight to {{ ticket.destination }}</h3>
                          <p class="text-white opacity-75 mb-0">
                            <span class="me-2">{{ formatDate(ticket.date) }}</span>
                            <span class="badge bg-primary bg-opacity-25 text-primary">{{ ticket.flightNumber }}</span>
                          </p>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-4 text-md-end mt-3 mt-md-0">
                      <button @click="toggleTicketDetails(ticket.id)" class="btn btn-outline-light btn-sm rounded-pill px-3">
                        <span v-if="expandedTicketId === ticket.id">Hide Details</span>
                        <span v-else>View Details</span>
                      </button>
                      <button v-if="ticket.status === 'upcoming'" @click="downloadTicket(ticket)" class="btn btn-glow btn-sm rounded-pill px-3 ms-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download me-1" viewBox="0 0 16 16">
                          <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                          <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                        </svg>
                        Ticket
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Ticket Details (Expandable) -->
                <div v-if="expandedTicketId === ticket.id" class="ticket-details">
                  <hr class="m-0 opacity-25">

                  <!-- Flight Information -->
                  <div class="p-4">
                    <div class="row">
                      <div class="col-md-8">
                        <div class="flight-route mb-4">
                          <div class="d-flex align-items-center">
                            <div class="flight-point">
                              <div class="airport-code">{{ ticket.departureCode }}</div>
                              <div class="airport-name text-white opacity-75">{{ ticket.departureCity }}</div>
                              <div class="flight-time text-white">{{ ticket.departureTime }}</div>
                            </div>

                            <div class="flight-path mx-3">
                              <div class="flight-line"></div>
                              <div class="flight-icon">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-airplane" viewBox="0 0 16 16">
                                  <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
                                </svg>
                              </div>
                              <div class="flight-duration text-white opacity-75">{{ ticket.duration }}</div>
                            </div>

                            <div class="flight-point">
                              <div class="airport-code">{{ ticket.arrivalCode }}</div>
                              <div class="airport-name text-white opacity-75">{{ ticket.destination }}</div>
                              <div class="flight-time text-white">{{ ticket.arrivalTime }}</div>
                            </div>
                          </div>
                        </div>

                        <!-- Passenger Information -->
                        <div class="passenger-info mb-4">
                          <h4 class="fs-5 fw-semibold text-white mb-3">Passenger Information</h4>
                          <div class="row g-3">
                            <div class="col-md-6">
                              <div class="info-item">
                                <div class="info-label text-white opacity-75">Passenger Name</div>
                                <div class="info-value text-white">{{ ticket.passengerName }}</div>
                              </div>
                            </div>
                            <div class="col-md-6">
                              <div class="info-item">
                                <div class="info-label text-white opacity-75">Passenger ID</div>
                                <div class="info-value text-white">{{ ticket.passengerId }}</div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- Seat Information -->
                        <div class="seat-info">
                          <h4 class="fs-5 fw-semibold text-white mb-3">Seat Information</h4>
                          <div class="row g-3">
                            <div v-for="(seat, index) in ticket.seats" :key="index" class="col-md-4">
                              <div class="seat-card p-3 rounded-3">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                  <div class="seat-number fs-5 fw-bold text-white">{{ seat.id }}</div>
                                  <div :class="`seat-class-dot ${seat.class}`"></div>
                                </div>
                                <div class="seat-class-name text-white opacity-75">{{ getSeatClassName(seat.class) }}</div>
                                <div class="seat-price text-white mt-1">${{ seat.price.toFixed(2) }}</div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- Enhanced Additional Services Section -->
                        <div class="services-info mt-4">
                          <h4 class="fs-5 fw-semibold text-white mb-3">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-stars me-2" viewBox="0 0 16 16">
                              <path d="M7.657 6.247c.11-.33.576-.33.686 0l.645 1.937a2.89 2.89 0 0 0 1.829 1.828l1.936.645c.33.11.33.576 0 .686l-1.937.645a2.89 2.89 0 0 0-1.828 1.829l-.645 1.936a.361.361 0 0 1-.686 0l-.645-1.937a2.89 2.89 0 0 0-1.828-1.828l-1.937-.645a.361.361 0 0 1 0-.686l1.937-.645a2.89 2.89 0 0 0 1.828-1.828l.645-1.937zM3.794 1.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387A1.734 1.734 0 0 0 4.593 5.69l-.387 1.162a.217.217 0 0 1-.412 0L3.407 5.69A1.734 1.734 0 0 0 2.31 4.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387A1.734 1.734 0 0 0 3.407 2.31l.387-1.162zM10.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732L9.1 2.137a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L10.863.1z"/>
                            </svg>
                            Additional Services
                          </h4>

                          <!-- Services Tabs -->
                          <div class="services-tabs mb-3">
                            <div class="btn-group w-100">
                              <button
                                @click="activeServiceTab = 'meals'"
                                :class="['btn', 'btn-sm', activeServiceTab === 'meals' ? 'btn-glow' : 'btn-outline-light']"
                                style="border-top-left-radius: 8px; border-bottom-left-radius: 8px"
                              >
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cup-hot me-1" viewBox="0 0 16 16">
                                  <path fill-rule="evenodd" d="M.5 6a.5.5 0 0 0-.488.608l1.652 7.434A2.5 2.5 0 0 0 4.104 16h5.792a2.5 2.5 0 0 0 2.44-1.958l.131-.59a3 3 0 0 0 1.3-5.854l.221-.99A.5.5 0 0 0 13.5 6H.5ZM13 12.5a2.01 2.01 0 0 1-.316-.025l.867-3.898A2.001 2.001 0 0 1 13 12.5ZM2.64 13.825 1.123 7h11.754l-1.517 6.825A1.5 1.5 0 0 1 9.896 15H4.104a1.5 1.5 0 0 1-1.464-1.175Z"/>
                                  <path d="m4.4.8-.003.004-.014.019a4.167 4.167 0 0 0-.204.31 2.327 2.327 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.31 3.31 0 0 1-.202.388 5.444 5.444 0 0 1-.253.382l-.018.025-.005.008-.002.002A.5.5 0 0 1 3.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 3.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 3 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 4.4.8Zm3 0-.003.004-.014.019a4.167 4.167 0 0 0-.204.31 2.327 2.327 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.31 3.31 0 0 1-.202.388 5.444 5.444 0 0 1-.253.382l-.018.025-.005.008-.002.002A.5.5 0 0 1 6.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 6.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 6 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 7.4.8Zm3 0-.003.004-.014.019a4.077 4.077 0 0 0-.204.31 2.337 2.337 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.198 3.198 0 0 1-.202.388 5.385 5.385 0 0 1-.252.382l-.019.025-.005.008-.002.002A.5.5 0 0 1 9.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 9.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 9 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 10.4.8Z"/>
                                </svg>
                                Meals & Drinks
                                <span v-if="hasAdditionalServices(ticket, 'meals')" class="badge bg-primary ms-1">{{ ticket.additional_services.meals.length }}</span>
                              </button>
                              <button
                                @click="activeServiceTab = 'baggage'"
                                :class="['btn', 'btn-sm', activeServiceTab === 'baggage' ? 'btn-glow' : 'btn-outline-light']">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-briefcase me-1" viewBox="0 0 16 16">
                                  <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l6.614 1.764a1.5 1.5 0 0 0 .772 0zM1.5 4h13a.5.5 0 0 1 .5.5v1.616L8.129 7.948a.5.5 0 0 1-.258 0L1 6.116V4.5a.5.5 0 0 1 .5-.5z"/>
                                </svg>
                                Baggage
                                <span v-if="hasAdditionalServices(ticket, 'baggage')" class="badge bg-primary ms-1">{{ ticket.additional_services.baggage.length }}</span>
                              </button>
                              <button
                                @click="activeServiceTab = 'comforts'"
                                :class="['btn', 'btn-sm', 'btn-right', activeServiceTab === 'comforts' ? 'btn-glow' : 'btn-outline-light']">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-emoji-smile me-1" viewBox="0 0 16 16">
                                  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                  <path d="M4.285 9.567a.5.5 0 0 1 .683.183A3.498 3.498 0 0 0 8 11.5a3.498 3.498 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.498 4.498 0 0 1 8 12.5a4.498 4.498 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683zM7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5zm4 0c0 .828-.448 1.5-1 1.5s-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5z"/>
                                </svg>
                                Comforts
                                <span v-if="hasAdditionalServices(ticket, 'comforts')" class="badge bg-primary ms-1">{{ ticket.additional_services.comforts.length }}</span>
                              </button>
                            </div>
                          </div>

                          <!-- No Services Message -->
                          <div v-if="!hasAnyAdditionalServices(ticket)" class="text-center py-4">
                            <div class="empty-service-icon mb-3">
                              <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-inbox text-primary opacity-50" viewBox="0 0 16 16">
                                <path d="M4.98 4a.5.5 0 0 0-.39.188L1.54 8H6a.5.5 0 0 1 .5.5 1.5 1.5 0 1 0 3 0A.5.5 0 0 1 10 8h4.46l-3.05-3.812A.5.5 0 0 0 11.02 4H4.98zm-1.17-.437A1.5 1.5 0 0 1 4.98 3h6.04a1.5 1.5 0 0 1 1.17.563l3.7 4.625a.5.5 0 0 1 .106.374l-.39 3.124A1.5 1.5 0 0 1 14.117 13H1.883a1.5 1.5 0 0 1-1.489-1.314l-.39-3.124a.5.5 0 0 1 .106-.374l3.7-4.625z"/>
                              </svg>
                            </div>
                            <p class="text-white opacity-75">No additional services have been added to this ticket.</p>
                          </div>

                          <!-- Services Content -->
                          <div v-else>
                            <!-- Meals Tab Content -->
                            <div v-if="activeServiceTab === 'meals'" class="service-tab-content">
                              <div v-if="!hasAdditionalServices(ticket, 'meals')" class="text-center py-3">
                                <p class="text-white opacity-75">No meal services selected for this flight.</p>
                              </div>
                              <div v-else class="row g-3">
                                <div v-for="(meal, index) in ticket.additional_services.meals" :key="'meal-' + index" class="col-md-4">
                                  <div class="service-card meal-card p-3 rounded-3">
                                    <div class="service-card-image mb-2" v-if="meal.image">
                                      <img :src="meal.image" class="img-fluid rounded" alt="Meal image">
                                    </div>
                                    <div v-else class="service-card-icon mb-2">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-cup-hot-fill text-primary" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M.5 6a.5.5 0 0 0-.488.608l1.652 7.434A2.5 2.5 0 0 0 4.104 16h5.792a2.5 2.5 0 0 0 2.44-1.958l.131-.59a3 3 0 0 0 1.3-5.854l.221-.99A.5.5 0 0 0 13.5 6H.5ZM13 12.5a2.01 2.01 0 0 1-.316-.025l.867-3.898A2.001 2.001 0 0 1 13 12.5Z"/>
                                        <path d="m4.4.8-.003.004-.014.019a4.167 4.167 0 0 0-.204.31 2.327 2.327 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.31 3.31 0 0 1-.202.388 5.444 5.444 0 0 1-.253.382l-.018.025-.005.008-.002.002A.5.5 0 0 1 3.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 3.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 3 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 4.4.8Zm3 0-.003.004-.014.019a4.167 4.167 0 0 0-.204.31 2.327 2.327 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.31 3.31 0 0 1-.202.388 5.444 5.444 0 0 1-.253.382l-.018.025-.005.008-.002.002A.5.5 0 0 1 6.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 6.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 6 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 7.4.8Zm3 0-.003.004-.014.019a4.077 4.077 0 0 0-.204.31 2.337 2.337 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.198 3.198 0 0 1-.202.388 5.385 5.385 0 0 1-.252.382l-.019.025-.005.008-.002.002A.5.5 0 0 1 9.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 9.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 9 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 10.4.8Z"/>
                                      </svg>
                                    </div>
                                    <div class="service-card-content">
                                      <h5 class="service-title text-white fw-bold mb-1">{{ meal.name }}</h5>
                                      <div class="service-details text-white opacity-75 mb-2">
                                        <div class="dietary-tags">
                                          <span v-for="(tag, tagIndex) in meal.dietaryOptions" :key="tagIndex" class="dietary-tag">
                                            {{ tag }}{{ tagIndex < meal.dietaryOptions.length - 1 ? ', ' : '' }}
                                          </span>
                                        </div>
                                        <div class="meal-description" v-if="meal.description">
                                          {{ meal.description }}
                                        </div>
                                      </div>
                                      <div class="service-price text-white fw-semibold">${{ meal.price.toFixed(2) }}</div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>

                            <!-- Baggage Tab Content -->
                            <div v-if="activeServiceTab === 'baggage'" class="service-tab-content">
                              <div v-if="!hasAdditionalServices(ticket, 'baggage')" class="text-center py-3">
                                <p class="text-white opacity-75">No additional baggage selected for this flight.</p>
                              </div>
                              <div v-else class="row g-3">
                                <div v-for="(bag, index) in ticket.additional_services.baggage" :key="'bag-' + index" class="col-md-4">
                                  <div class="service-card baggage-card p-3 rounded-3">
                                    <div class="service-card-icon mb-2">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-briefcase-fill text-primary" viewBox="0 0 16 16">
                                        <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v1.384l7.614 2.03a1.5 1.5 0 0 0 .772 0L16 5.884V4.5A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5z"/>
                                        <path d="M0 12.5A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5V6.85L8.129 8.947a.5.5 0 0 1-.258 0L0 6.85v5.65z"/>
                                      </svg>
                                    </div>
                                    <div class="service-card-content">
                                      <h5 class="service-title text-white fw-bold mb-1">{{ bag.name }}</h5>
                                      <div class="service-details text-white opacity-75 mb-2">
                                        <div class="baggage-weight">
                                          <span class="weight-value">{{ bag.weight }}kg</span>
                                          <span v-if="bag.dimensions" class="dimensions ms-2">({{ bag.dimensions }})</span>
                                        </div>
                                        <div class="baggage-description" v-if="bag.description">
                                          {{ bag.description }}
                                        </div>
                                      </div>
                                      <div class="service-price text-white fw-semibold">${{ bag.price.toFixed(2) }}</div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>

                            <!-- Comforts Tab Content -->
                            <div v-if="activeServiceTab === 'comforts'" class="service-tab-content">
                              <div v-if="!hasAdditionalServices(ticket, 'comforts')" class="text-center py-3">
                                <p class="text-white opacity-75">No comfort services selected for this flight.</p>
                              </div>
                              <div v-else class="row g-3">
                                <div v-for="(comfort, index) in ticket.additional_services.comforts" :key="'comfort-' + index" class="col-md-4">
                                  <div class="service-card comfort-card p-3 rounded-3">
                                    <div class="service-card-icon mb-2">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-emoji-smile-fill text-primary" viewBox="0 0 16 16">
                                        <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zM7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5zM4.285 9.567a.5.5 0 0 1 .683.183A3.498 3.498 0 0 0 8 11.5a3.498 3.498 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.498 4.498 0 0 1 8 12.5a4.498 4.498 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683zM10 8c-.552 0-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5S10.552 8 10 8z"/>
                                      </svg>
                                    </div>
                                    <div class="service-card-content">
                                      <h5 class="service-title text-white fw-bold mb-1">{{ comfort.name }}</h5>
                                      <div class="service-details text-white opacity-75 mb-2">
                                        <div class="comfort-description">
                                          {{ comfort.description }}
                                        </div>
                                      </div>
                                      <div class="service-price text-white fw-semibold">${{ comfort.price.toFixed(2) }}</div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>

                          <!-- Total Services Price -->
                          <div v-if="hasAnyAdditionalServices(ticket)" class="services-total mt-3 text-end">
                            <div class="text-white opacity-75">
                              Additional Services Total:
                              <span class="fw-bold text-primary">${{ calculateAdditionalServicesTotal(ticket).toFixed(2) }}</span>
                            </div>
                          </div>
                        </div>

                      </div>

                      <!-- Boarding Pass Preview -->
                      <div class="col-md-4 mt-4 mt-md-0">
                        <div class="boarding-pass">
                          <div class="boarding-pass-header">
                            <div class="airline-name">DjangoAIR</div>
                            <div class="boarding-title">BOARDING PASS</div>
                          </div>
                          <div class="boarding-pass-body">
                            <div class="boarding-row">
                              <div class="boarding-label">PASSENGER</div>
                              <div class="boarding-value">{{ ticket.passengerName }}</div>
                            </div>
                            <div class="boarding-row">
                              <div class="boarding-col">
                                <div class="boarding-label">FLIGHT</div>
                                <div class="boarding-value">{{ ticket.flightNumber }}</div>
                              </div>
                              <div class="boarding-col">
                                <div class="boarding-label">DATE</div>
                                <div class="boarding-value">{{ formatShortDate(ticket.date) }}</div>
                              </div>
                            </div>
                            <div class="boarding-row">
                              <div class="boarding-col">
                                <div class="boarding-label">FROM</div>
                                <div class="boarding-value">{{ ticket.departureCode }}</div>
                              </div>
                              <div class="boarding-col">
                                <div class="boarding-label">TO</div>
                                <div class="boarding-value">{{ ticket.arrivalCode }}</div>
                              </div>
                            </div>
                            <div class="boarding-row">
                              <div class="boarding-col">
                                <div class="boarding-label">SEAT</div>
                                <div class="boarding-value">{{ ticket.seats[0]?.id || 'N/A' }}</div>
                              </div>
                              <div class="boarding-col">
                                <div class="boarding-label">GATE</div>
                                <div class="boarding-value">{{ ticket.gate }}</div>
                              </div>
                            </div>
                            <div class="boarding-row">
                              <div class="boarding-col">
                                <div class="boarding-label">BOARDING</div>
                                <div class="boarding-value">{{ ticket.boardingTime }}</div>
                              </div>
                              <div class="boarding-col">
                                <div class="boarding-label">DEPARTURE</div>
                                <div class="boarding-value">{{ ticket.departureTime }}</div>
                              </div>
                            </div>
                          </div>
                          <div class="boarding-pass-footer">
                            <div >
                              <svg :id="`barcode-${ticket.id}`" class="barcode"></svg>
                            </div>
                            <div class="boarding-ref">REF: {{ ticket.bookingReference }}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Ticket Actions -->
                  <hr class="m-0 opacity-25">
                  <div class="ticket-actions p-3 d-flex justify-content-end">
                    <button v-if="ticket.status === 'upcoming'" @click="showCancelConfirmation(ticket.id)" class="btn btn-outline-danger btn-sm rounded-pill px-3">
                      Cancel Booking
                    </button>
                    <button v-if="ticket.status === 'upcoming'"
                            @click="downloadTicket(ticket)"
                            class="btn btn-glow btn-sm rounded-pill px-3 ms-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download me-1" viewBox="0 0 16 16">
                        <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                        <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                      </svg>
                      Download Ticket
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div class="d-flex justify-content-center mt-5">
            <nav aria-label="Tickets pagination">
              <ul class="pagination">
                <li :class="['page-item', { disabled: currentPage === 1 }]">
                  <button @click="changePage(currentPage - 1)" class="page-link" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                  </button>
                </li>
                <li v-for="page in totalPages" :key="page" :class="['page-item', { active: currentPage === page }]">
                  <button @click="changePage(page)" class="page-link">{{ page }}</button>
                </li>
                <li :class="['page-item', { disabled: currentPage === totalPages }]">
                  <button @click="changePage(currentPage + 1)" class="page-link" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Cancel Confirmation Modal -->
  <div v-if="showCancelModal" class="modal-backdrop">
    <div class="cancel-modal">
      <div class="cancel-modal-content">
        <h4 class="fs-5 fw-semibold text-white mb-3">Cancel Booking</h4>
        <p class="text-white opacity-75 mb-4">Are you sure you want to cancel this booking? This action cannot be undone.</p>
        <div class="d-flex justify-content-end">
          <button @click="closeCancelModal" class="btn btn-outline-light btn-sm rounded-pill px-3 me-2">
            No, Keep Booking
          </button>
          <button @click="confirmCancelBooking" class="btn btn-danger btn-sm rounded-pill px-3">
            Yes, Cancel Booking
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import JsBarcode from 'jsbarcode';
import ticketGeneration from "@/scripts/ticketGeneration";

export default {
  data() {
    return {
      /**
       * Authentication state and user data
       */
      isAuthenticated: false, // Set to true for demo purposes
      userData: {
        name: '',
        email: '',
        id: null,
      },
      isGeneratingPDF: false,
      toastMessage: '',
      errorMessage: '',
      isProfileMenuOpen: false,
      showAuthRequiredMessage: false,

      /**
       * Tickets data and display state
       */
      tickets: [], // Will be populated from API
      isLoading: true,
      expandedTicketId: null,
      showCancelModal: false,
      ticketToCancel: null,

      /**
       * Filtering and pagination
       */
      filterStatus: 'all',
      sortBy: 'date-desc',
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 5,

      /**
       * Additional services display
       */
      activeServiceTab: 'meals',

      /**
       * Sample data for demonstration
       */
      sampleTickets: [
        {
          id: 1,
          destination: 'Paris',
          departureCity: 'New York',
          departureCode: 'JFK',
          arrivalCode: 'CDG',
          date: '2025-05-20',
          departureTime: '08:30',
          arrivalTime: '21:45',
          duration: '7h 15m',
          flightNumber: 'DA1234',
          status: 'upcoming',
          passengerName: 'John Doe',
          passengerId: 'P12345678',
          bookingReference: 'ABCDEF',
          gate: 'B12',
          boardingTime: '08:00',
          seats: [
            { id: '1A', class: 'first', price: 250 },
            { id: '1B', class: 'first', price: 250 }
          ],
          additional_services: {
            meals: [
              {
                name: 'Premium Dinner',
                price: 35.00,
                dietaryOptions: ['Vegetarian', 'Gluten-free'],
                description: 'Gourmet 3-course meal with wine pairing',
                image: '/images/meals/premium-dinner.jpg'
              },
              {
                name: 'Continental Breakfast',
                price: 15.00,
                dietaryOptions: ['Vegan'],
                description: 'Fresh pastries, fruits, and coffee'
              }
            ],
            baggage: [
              {
                name: 'Extra Checked Bag',
                price: 50.00,
                weight: 23,
                dimensions: '62 linear inches',
                description: 'Additional checked baggage allowance'
              }
            ],
            comforts: [
              {
                name: 'Priority Boarding',
                price: 25.00,
                description: 'Be among the first to board the aircraft'
              },
              {
                name: 'In-flight Wi-Fi',
                price: 12.00,
                description: 'Full flight internet access'
              }
            ]
          },
          totalAmount: 500
        },
        {
          id: 2,
          destination: 'London',
          departureCity: 'New York',
          departureCode: 'JFK',
          arrivalCode: 'LHR',
          date: '2025-06-15',
          departureTime: '10:15',
          arrivalTime: '22:30',
          duration: '6h 15m',
          flightNumber: 'DA2345',
          status: 'upcoming',
          passengerName: 'John Doe',
          passengerId: 'P12345678',
          bookingReference: 'BCDEFG',
          gate: 'C15',
          boardingTime: '09:45',
          seats: [
            { id: '3C', class: 'business', price: 150 }
          ],
          additional_services: {
            meals: [],
            baggage: [
              {
                name: 'Extra Carry-on',
                price: 30.00,
                weight: 10,
                description: 'Additional small carry-on bag'
              }
            ],
            comforts: []
          },
          totalAmount: 150
        },
        {
          id: 3,
          destination: 'Tokyo',
          departureCity: 'New York',
          departureCode: 'JFK',
          arrivalCode: 'HND',
          date: '2025-04-10',
          departureTime: '14:20',
          arrivalTime: '17:45',
          duration: '13h 25m',
          flightNumber: 'DA3456',
          status: 'past',
          passengerName: 'John Doe',
          passengerId: 'P12345678',
          bookingReference: 'CDEFGH',
          gate: 'A22',
          boardingTime: '13:50',
          seats: [
            { id: '5D', class: 'economy', price: 75 },
            { id: '5E', class: 'economy', price: 75 },
            { id: '5F', class: 'economy', price: 75 }
          ],
          additional_services: {
            meals: [
              {
                name: 'Asian Cuisine Special',
                price: 28.00,
                dietaryOptions: ['Spicy', 'Contains seafood'],
                description: 'Authentic Asian dishes prepared by our chef'
              }
            ],
            baggage: [],
            comforts: [
              {
                name: 'Comfort Kit',
                price: 15.00,
                description: 'Eye mask, earplugs, neck pillow, and blanket'
              }
            ]
          },
          totalAmount: 225
        },
        {
          id: 4,
          destination: 'Sydney',
          departureCity: 'New York',
          departureCode: 'JFK',
          arrivalCode: 'SYD',
          date: '2025-03-05',
          departureTime: '22:10',
          arrivalTime: '06:30',
          duration: '22h 20m',
          flightNumber: 'DA4567',
          status: 'canceled',
          passengerName: 'John Doe',
          passengerId: 'P12345678',
          bookingReference: 'DEFGHI',
          gate: 'D05',
          boardingTime: '21:40',
          seats: [
            { id: '10A', class: 'economy', price: 75 }
          ],
          additional_services: {
            meals: [],
            baggage: [],
            comforts: []
          },
          totalAmount: 75
        },
        {
          id: 5,
          destination: 'Rome',
          departureCity: 'New York',
          departureCode: 'JFK',
          arrivalCode: 'FCO',
          date: '2025-07-22',
          departureTime: '12:45',
          arrivalTime: '02:15',
          duration: '7h 30m',
          flightNumber: 'DA5678',
          status: 'upcoming',
          passengerName: 'John Doe',
          passengerId: 'P12345678',
          bookingReference: 'EFGHIJ',
          gate: 'B08',
          boardingTime: '12:15',
          seats: [
            { id: '2F', class: 'first', price: 250 }
          ],
          additional_services: {
            meals: [
              {
                name: 'Italian Cuisine',
                price: 32.00,
                dietaryOptions: ['Mediterranean', 'Organic'],
                description: 'Authentic Italian dishes with local ingredients'
              }
            ],
            baggage: [
              {
                name: 'Sports Equipment',
                price: 45.00,
                weight: 20,
                description: 'Special handling for sports equipment'
              }
            ],
            comforts: [
              {
                name: 'Premium Headphones',
                price: 8.00,
                description: 'Noise-cancelling headphones for your journey'
              }
            ]
          },
          totalAmount: 250
        },
        {
          id: 6,
          destination: 'Dubai',
          departureCity: 'New York',
          departureCode: 'JFK',
          arrivalCode: 'DXB',
          date: '2025-02-18',
          departureTime: '01:30',
          arrivalTime: '20:45',
          duration: '13h 15m',
          flightNumber: 'DA6789',
          status: 'past',
          passengerName: 'John Doe',
          passengerId: 'P12345678',
          bookingReference: 'FGHIJK',
          gate: 'E11',
          boardingTime: '01:00',
          seats: [
            { id: '4B', class: 'business', price: 150 },
            { id: '4C', class: 'business', price: 150 }
          ],
          additional_services: {
            meals: [
              {
                name: 'Middle Eastern Feast',
                price: 30.00,
                dietaryOptions: ['Halal', 'Spicy option'],
                description: 'Traditional Middle Eastern cuisine'
              }
            ],
            baggage: [
              {
                name: 'Excess Weight',
                price: 75.00,
                weight: 15,
                description: 'Additional weight allowance for checked baggage'
              }
            ],
            comforts: [
              {
                name: 'Lounge Access',
                price: 50.00,
                description: 'Access to premium airport lounge before departure'
              }
            ]
          },
          totalAmount: 300
        }
      ]
    };
  },

  computed: {
    /**
     * Calculates user initials from the user's name for the avatar display
     * @returns {string} User initials or '?' if name is not available
     */
    userInitials() {
      if (!this.userData.name) return '?';
      return this.userData.name.split(' ')
        .map(name => name.charAt(0).toUpperCase())
        .slice(0, 2)
        .join('');
    },

    /**
     * Filters and sorts tickets based on user-selected criteria
     * @returns {Array} Filtered and sorted array of ticket objects
     */
    filteredTickets() {
      // Start with all tickets
      let result = [...this.tickets];

      // Apply status filter
      if (this.filterStatus !== 'all') {
        result = result.filter(ticket => ticket.status === this.filterStatus);
      }

      // Apply search filter
      if (this.searchQuery.trim() !== '') {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(ticket =>
          ticket.destination.toLowerCase().includes(query) ||
          ticket.flightNumber.toLowerCase().includes(query) ||
          ticket.bookingReference.toLowerCase().includes(query)
        );
      }

      // Apply sorting
      result.sort((a, b) => {
        switch (this.sortBy) {
          case 'date-asc':
            return new Date(a.date) - new Date(b.date);
          case 'date-desc':
            return new Date(b.date) - new Date(a.date);
          case 'destination':
            return a.destination.localeCompare(b.destination);
          default:
            return 0;
        }
      });

      return result;
    },

    /**
     * Returns paginated tickets based on current page and items per page
     * @returns {Array} Paginated array of ticket objects
     */
    paginatedTickets() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredTickets.slice(startIndex, endIndex);
    },

    /**
     * Calculates the total number of pages based on filtered tickets and items per page
     * @returns {number} Total number of pages
     */
    totalPages() {
      return Math.ceil(this.filteredTickets.length / this.itemsPerPage);
    }
  },

  methods: {
    /**
     * Toggles the user profile dropdown menu visibility
     */
    showUserProfile() {
      this.isProfileMenuOpen = !this.isProfileMenuOpen;
    },

    /**
     * Closes the profile menu when clicking outside of it
     * @param {Event} event - The click event object
     */
    closeProfileMenu(event) {
      if (this.isProfileMenuOpen && !event.target.closest('.user-profile-container')) {
        this.isProfileMenuOpen = false;
      }
    },

    /**
     * Handles user logout process
     * Clears authentication state, user data, and localStorage
     * Makes a logout request to the server
     * Redirects to the home page
     */
    logout() {
      this.isAuthenticated = false;
      this.userData = {
        name: '',
        email: '',
        id: null
      };
      this.isProfileMenuOpen = false;

      // Remove authentication data from localStorage
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userData');

      // Make server request for logout
      fetch('/auth/logout/', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          console.log('Logout successful:', data);
          // Redirect to home page
          window.location.href = '/';
        })
        .catch(error => {
          console.error('Logout error:', error);
        });
    },

    /**
     * Closes the authentication required message
     */
    closeAuthRequiredMessage() {
      this.showAuthRequiredMessage = false;
    },

    /**
     * Opens the login modal dialog
     */
    openLoginModal() {
      this.showAuthRequiredMessage = false;
      // Implementation would depend on your authentication component
      console.log('Open login modal');
    },

    /**
     * Opens the registration modal dialog
     */
    openRegisterModal() {
      this.showAuthRequiredMessage = false;
      // Implementation would depend on your authentication component
      console.log('Open register modal');
    },

    /**
     * Formats date string for display in the UI
     * @param {string} dateString - ISO date string to format
     * @returns {string} Formatted date string or empty string if input is falsy
     */
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    /**
     * Formats date string in a shorter format (MM/DD/YYYY)
     * @param {string} dateString - ISO date string to format
     * @returns {string} Formatted date string or empty string if input is falsy
     */
    formatShortDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric'
      });
    },

    /**
     * Formats ticket status for display
     * @param {string} status - Status code (upcoming, past, cancelled)
     * @returns {string} User-friendly status text
     */
    formatStatus(status) {
      switch (status) {
        case 'upcoming': return 'Upcoming';
        case 'late': return 'Late';
        case 'canceled': return 'Canceled';
        case 'used': return 'Used';
        case 'boarded': return 'Boarded';
        case 'checked_in': return 'Checked-in';
        default: return status.charAt(0).toUpperCase() + status.slice(1);
      }
    },

    /**
     * Gets the display name for a seat class
     * @param {string} seatClass - Internal class name (first, business, economy)
     * @returns {string} User-friendly class name for display
     */
    getSeatClassName(seatClass) {
      switch(seatClass) {
        case 'first': return 'First Class';
        case 'business': return 'Business Class';
        case 'economy': return 'Economy';
        default: return 'Economy';
      }
    },

    /**
     * Toggles the expanded state of a ticket to show/hide details
     * @param {number|string} ticketId - ID of the ticket to toggle
     */
    toggleTicketDetails(ticketId) {
      if (this.expandedTicketId === ticketId) {
        this.expandedTicketId = null;
      } else {
        this.expandedTicketId = ticketId;

        this.$nextTick(() => {
          const barcodeElement = document.getElementById(`barcode-${ticketId}`);
          const ticket = this.tickets.find(t => t.id === ticketId);

          console.log(ticket);
          console.log(barcodeElement);

          const barcodeURL = `barcode/${ticket.bookingReference}`;

          if (barcodeElement && ticket?.bookingReference) {
            JsBarcode(barcodeElement, barcodeURL, {
              format: "CODE128",
              lineColor: "#ffffff",
              width: 1.0,
              height: 40,
              displayValue: false
            });
          }

          const bgRect = barcodeElement.querySelector('rect');
          if (bgRect) {
            bgRect.style.fill = 'transparent';  // або можна повністю прибрати rect: bgRect.remove();
          }
        });
      }
    },

    /**
     * Changes the current page in pagination
     * @param {number} page - Page number to navigate to
     */
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      // Scroll to top of tickets list
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    /**
     * Resets all filters to their default values
     */
    resetFilters() {
      this.filterStatus = 'all';
      this.sortBy = 'date-desc';
      this.searchQuery = '';
      this.currentPage = 1;
    },

    /**
     * Shows the cancel confirmation modal for a specific ticket
     * @param {number|string} ticketId - ID of the ticket to cancel
     */
    showCancelConfirmation(ticketId) {
      this.ticketToCancel = ticketId;
      this.showCancelModal = true;
    },

    /**
     * Closes the cancel confirmation modal
     */
    closeCancelModal() {
      this.showCancelModal = false;
      this.ticketToCancel = null;
    },

    /**
     * Confirms the cancellation of a booking
     * Makes an API request to cancel the booking and updates the UI
     */
    async confirmCancelBooking() {
      if (!this.ticketToCancel) return;

      fetch('/api/cancel-ticket/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken')
        },
        body: JSON.stringify({ ticket_id: this.ticketToCancel }),
      })
          .then(response => response.json())
          .then(data => {
            // For demo purposes, update the ticket status locally
            const ticketIndex = this.tickets.findIndex(ticket => ticket.id === this.ticketToCancel);
            if (ticketIndex !== -1) {
              this.tickets[ticketIndex].status = 'canceled';
            }
          })
          .catch(error => {
            this.errorMessage = data.error_message;
          });

      // Close the modal
      this.closeCancelModal();
    },

    /**
     * Simulates downloading a ticket
     * In a real application, this would generate a PDF or redirect to a download endpoint
     * @param {Object} ticket - Ticket object containing all ticket details
     */
    async downloadTicket(ticket) {
      console.log(`Downloading ticket for flight ${ticket.flightNumber} to ${ticket.destination}`);

      try {
        // Показуємо індикатор завантаження
        this.isGeneratingPDF = true;

        // Викликаємо сервіс для генерації PDF
        const success = await ticketGeneration.generateTicketPDF(ticket);

        console.log(ticket);

        if (success) {
          // Показуємо повідомлення про успіх
          this.showSuccessToast('Ticket downloaded successfully!');
        } else {
          // Показуємо повідомлення про помилку
          this.showErrorToast('Failed to generate ticket. Please try again.');
        }
      } catch (error) {
        console.error('Error downloading ticket:', error);
        this.showErrorToast(`An error occurred: ${error.message}`);
      } finally {
        // Приховуємо індикатор завантаження
        this.isGeneratingPDF = false;
      }
    },

    /**
     * Checks if a ticket has additional services of a specific type
     * @param {Object} ticket - Ticket object
     * @param {string} serviceType - Type of service (meals, baggage, comforts)
     * @returns {boolean} True if the ticket has services of the specified type
     */
    hasAdditionalServices(ticket, serviceType) {
      if (!ticket.additional_services || !ticket.additional_services[serviceType]) {
        return false;
      }
      return ticket.additional_services[serviceType].length > 0;
    },

    /**
     * Checks if a ticket has any additional services
     * @param {Object} ticket - Ticket object
     * @returns {boolean} True if the ticket has any additional services
     */
    hasAnyAdditionalServices(ticket) {
      if (!ticket.additional_services) return false;

      return (
        this.hasAdditionalServices(ticket, 'meals') ||
        this.hasAdditionalServices(ticket, 'baggage') ||
        this.hasAdditionalServices(ticket, 'comforts')
      );
    },

    /**
     * Calculates the total price of all additional services for a ticket
     * @param {Object} ticket - Ticket object
     * @returns {number} Total price of all additional services
     */
    calculateAdditionalServicesTotal(ticket) {
      if (!ticket.additional_services) return 0;

      let total = 0;

      // Add up meal prices
      if (ticket.additional_services.meals) {
        total += ticket.additional_services.meals.reduce((sum, meal) => sum + meal.price, 0);
      }

      // Add up baggage prices
      if (ticket.additional_services.baggage) {
        total += ticket.additional_services.baggage.reduce((sum, bag) => sum + bag.price, 0);
      }

      // Add up comfort prices
      if (ticket.additional_services.comforts) {
        total += ticket.additional_services.comforts.reduce((sum, comfort) => sum + comfort.price, 0);
      }

      return total;
    },

    showSuccessToast(message) {
      this.toastMessage = message;
      const toastEl = this.$refs.successToast;
      if (toastEl && window.bootstrap) {
        const toast = new window.bootstrap.Toast(toastEl);
        toast.show();
      } else {
      }
    },

    showErrorToast(message) {
      this.errorMessage = message;
      const toastEl = this.$refs.errorToast;
      if (toastEl && window.bootstrap) {
        const toast = new window.bootstrap.Toast(toastEl);
        toast.show();
      } else {
        alert(`Error: ${message}`); // Fallback якщо toast не доступний
      }
    },

    /**
     * Fetches tickets from the API
     * In this demo, it uses sample data instead of making a real API call
     */
    fetchTickets() {
      this.isLoading = true;

      // Simulate API call with setTimeout
      // setTimeout(() => {
      //   // In a real application, you would fetch data from an API
      //   this.tickets = this.sampleTickets;
      //   this.isLoading = false;
      // }, 1500);

      // Real API call would look something like this:
      fetch('/api/get_tickets')
          .then(response => response.json())
          .then(data => {
            this.tickets = data;
            this.isLoading = false;
          })
          .catch(error => {
            console.error('Error fetching tickets:', error);
            this.isLoading = false;
          });
    },

    /**
     * Checks user authentication status from localStorage on page load
     * Redirects unauthenticated users or shows authentication required message
     */
    checkAuthentication() {
      // For demo purposes, we're assuming the user is authenticated
      // In a real application, you would check localStorage or make an API call

      const isAuth = localStorage.getItem('isAuthenticated') === 'true';
      const userDataStr = localStorage.getItem('userData');

      if (isAuth && userDataStr) {
        try {
          const userData = JSON.parse(userDataStr);
          this.isAuthenticated = true;
          this.userData = userData;
        } catch (e) {
          console.error('Error parsing user data:', e);
          this.isAuthenticated = false;
          this.showAuthRequiredMessage = true;
        }
      } else {
        // For demo purposes, we're not redirecting or showing the auth message
        // In a real application, you might do:
        // this.isAuthenticated = false;
        // this.showAuthRequiredMessage = true;
      }
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
  },

  mounted() {
    /**
     * Component mounted lifecycle hook
     * Fetches current user data from the server
     * Checks authentication status from localStorage
     * Initializes Bootstrap modal for success message
     * Sets up click event listener for closing the profile menu
     */
    // For demo purposes, we'll set some sample user data
    this.isAuthenticated = true;
    this.userData = {
      name: 'John Doe',
      email: 'john.doe@example.com',
      id: 123,
    };

    fetch('/api/current_user/')
        .then(response => response.json())
        .then(data => {
          this.isAuthenticated = data.isAuthenticated;
          this.userData = {
            name: data.user.name,
            email: data.user.email,
            id: data.user.id,
          };
        })
        .catch(error => {
          console.error('Failed to fetch user data:', error);
          this.isAuthenticated = false;
          this.userData = {
            id: null,
            name: '',
            email: '',
          };
        });

    this.fetchTickets();

    // Initialize Bootstrap modal for success message
    if (typeof bootstrap !== 'undefined') {
      this.modal = new bootstrap.Modal(document.getElementById('successModal'));
    }

    // Add click event listener for closing the profile menu
    document.addEventListener('click', this.closeProfileMenu);
  },

  beforeUnmount() {
    /**
     * Component beforeUnmount lifecycle hook
     * Removes event listeners to prevent memory leaks
     */
    document.removeEventListener('click', this.closeProfileMenu);
  },

  watch: {
    /**
     * Watches for changes in filter criteria and resets pagination
     */
    filterStatus() {
      this.currentPage = 1;
    },
    sortBy() {
      this.currentPage = 1;
    },
    searchQuery() {
      this.currentPage = 1;
    }
  }
};
</script>

<style scoped>
/* Base styles */
.tickets-app {
  --color-primary: #6c63ff;
  --color-secondary: #ff6584;
  --color-tertiary: #43cbff;
  --color-success: #00c9a7;
  --color-danger: #ff6b6b;
  --color-warning: #ffd166;
  --color-dark: #1a1a2e;
  --color-light: #f8f9fa;

  color: var(--color-light);
  font-family: 'Poppins', sans-serif;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* Main background that spans all sections */
.main-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  z-index: 0;
  overflow: hidden;
}

/* Stars background */
.stars-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(2px 2px at calc(random(100) * 1vw) calc(random(100) * 1vh), white, rgba(0, 0, 0, 0)),
  radial-gradient(2px 2px at calc(random(100) * 1vw) calc(random(100) * 1vh), white, rgba(0, 0, 0, 0)),
  radial-gradient(2px 2px at calc(random(100) * 1vw) calc(random(100) * 1vh), white, rgba(0, 0, 0, 0));
  background-size: 100% 100%;
  background-repeat: no-repeat;
}

.stars-1 {
  opacity: 0.3;
}

.stars-2 {
  opacity: 0.2;
  transform: rotate(30deg);
}

.stars-3 {
  opacity: 0.1;
  transform: rotate(60deg);
}

/* Animated shapes for background */
.animated-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.2;
  filter: blur(40px);
}

.shape-1 {
  width: 300px;
  height: 300px;
  background: var(--color-primary);
  top: 10%;
  left: 5%;
  animation: float 20s infinite alternate ease-in-out;
}

.shape-2 {
  width: 200px;
  height: 200px;
  background: var(--color-secondary);
  bottom: 10%;
  right: 5%;
  animation: float 15s infinite alternate-reverse ease-in-out;
}

.shape-3 {
  width: 150px;
  height: 150px;
  background: var(--color-tertiary);
  top: 30%;
  right: 10%;
  animation: float 18s infinite alternate ease-in-out;
}

.shape-4 {
  width: 250px;
  height: 250px;
  background: var(--color-primary);
  bottom: 20%;
  left: 10%;
  animation: float 22s infinite alternate-reverse ease-in-out;
}

.shape-5 {
  width: 180px;
  height: 180px;
  background: var(--color-tertiary);
  top: 45%;
  left: 45%;
  animation: float 25s infinite alternate ease-in-out;
}

/* Z-index utility */
.z-index-2 {
  z-index: 2;
}

/* Glass card effect */
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Text gradient */
.text-gradient {
  background: linear-gradient(90deg, var(--color-primary), var(--color-tertiary));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-fill-color: transparent;
}

.text-gradient-alt {
  background: linear-gradient(90deg, var(--color-tertiary), var(--color-primary));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-fill-color: transparent;
}

/* Glow effects */
.text-glow {
  color: var(--color-primary);
  text-shadow: 0 0 10px rgba(108, 99, 255, 0.5);
}

.btn-glow {
  background: linear-gradient(45deg, var(--color-primary), var(--color-tertiary));
  border: none;
  color: white;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(108, 99, 255, 0.4);
}

.btn-glow:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(108, 99, 255, 0.6);
}

.btn-glow:before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
  rgba(255, 255, 255, 0) 0%,
  rgba(255, 255, 255, 0.2) 50%,
  rgba(255, 255, 255, 0) 100%);
  transition: all 0.6s;
}

.btn-glow:hover:before {
  left: 100%;
}

/* Input group styling */
.input-group-glow {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.input-group-glow:focus-within {
  box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.5);
  border-color: var(--color-primary);
}

.input-group-glow .form-control,
.input-group-glow .input-group-text,
.input-group-glow .btn {
  background: transparent;
  border: none;
  color: var(--color-light);
}

.input-group-glow .form-control::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-control, .form-select {
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-light);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.5);
  border-color: var(--color-primary);
  background: rgba(255, 255, 255, 0.1);
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

/* Fix for select option text color */
.form-select option {
  background-color: var(--color-dark);
  color: var(--color-light);
}

/* User profile styles */
.user-profile-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.user-profile-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-tertiary));
  border: 2px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.user-profile-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

.user-avatar {
  font-weight: 600;
  font-size: 16px;
}

.profile-dropdown {
  position: absolute;
  top: 50px;
  right: 0;
  width: 220px;
  background: rgba(26, 26, 46, 0.95);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: fadeIn 0.3s ease;
}

.profile-header {
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-name {
  display: block;
  font-weight: 600;
  font-size: 14px;
  color: white;
  margin-bottom: 5px;
}

.profile-email {
  display: block;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.profile-menu-items {
  padding: 10px 0;
}

.profile-menu-item {
  display: block;
  padding: 10px 15px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s ease;
  font-size: 14px;
}

.profile-menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.profile-menu-item.active {
  background: rgba(108, 99, 255, 0.2);
  color: var(--color-primary);
}

.logout-button {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  color: #ff6584;
  cursor: pointer;
}

.logout-button:hover {
  background: rgba(255, 101, 132, 0.1);
}

/* Auth required message */
.auth-required-message {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.auth-required-content {
  width: 90%;
  max-width: 400px;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(20, 20, 35, 0.95));
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  position: relative;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: slideUp 0.4s ease;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 24px;
  cursor: pointer;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: white;
}

.auth-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-login, .btn-register {
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-login {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-login:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn-register {
  background: linear-gradient(45deg, var(--color-primary), var(--color-tertiary));
  border: none;
  color: white;
}

.btn-register:hover {
  box-shadow: 0 0 15px rgba(108, 99, 255, 0.5);
  transform: translateY(-2px);
}

/* Ticket card styles */
.ticket-card {
  position: relative;
  transition: all 0.3s ease;
}

.ticket-card:hover {
  transform: translateY(-5px);
}

.ticket-status-badge {
  position: absolute;
  top: 0;
  right: 20px;
  padding: 5px 15px;
  border-radius: 0 0 10px 10px;
  font-size: 12px;
  font-weight: 600;
  z-index: 1;
}

.ticket-status-badge.upcoming {
  background: rgba(0, 201, 167, 0.2);
  color: var(--color-success);
  border: 1px solid rgba(0, 201, 167, 0.3);
  border-top: none;
}

.ticket-status-badge.past {
  background: rgba(108, 99, 255, 0.2);
  color: var(--color-primary);
  border: 1px solid rgba(108, 99, 255, 0.3);
  border-top: none;
}

.ticket-status-badge.canceled {
  background: rgba(255, 107, 107, 0.2);
  color: var(--color-danger);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-top: none;
}

.ticket-header {
  position: relative;
}

.airline-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: rgba(108, 99, 255, 0.1);
  border-radius: 50%;
  color: var(--color-primary);
}

/* Flight route styles */
.flight-route {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flight-point {
  text-align: center;
}

.airport-code {
  font-size: 24px;
  font-weight: 700;
  color: white;
}

.airport-name {
  font-size: 14px;
  margin-bottom: 5px;
}

.flight-time {
  font-size: 16px;
  font-weight: 600;
}

.flight-path {
  position: relative;
  width: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.flight-line {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg,
  rgba(108, 99, 255, 0.3),
  rgba(108, 99, 255, 0.7),
  rgba(108, 99, 255, 0.3));
}

.flight-icon {
  position: absolute;
  top: -7px;
  color: var(--color-primary);
  background: rgba(26, 26, 46, 0.8);
  padding: 2px;
  border-radius: 50%;
  transform: rotate(90deg);
}

.flight-duration {
  font-size: 12px;
  margin-top: 5px;
}

/* Passenger and seat info styles */
.info-item {
  margin-bottom: 10px;
}

.info-label {
  font-size: 12px;
  margin-bottom: 2px;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
}

.seat-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.seat-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.seat-class-dot {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.seat-class-dot.first {
  background-color: rgba(255, 215, 0, 0.8);
}

.seat-class-dot.business {
  background-color: rgba(108, 99, 255, 0.8);
}

.seat-class-dot.economy {
  background-color: rgba(160, 160, 160, 0.8);
}

/* Service card styles */
.service-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.service-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.service-card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(108, 99, 255, 0.1);
  border-radius: 50%;
  margin-bottom: 10px;
}

.service-card-image {
  width: 100%;
  height: 120px;
  overflow: hidden;
  border-radius: 8px;
}

.service-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.service-title {
  font-size: 16px;
  margin-bottom: 5px;
}

.service-details {
  font-size: 12px;
  flex: 1;
}

.service-price {
  margin-top: auto;
  font-size: 16px;
  color: var(--color-primary);
}

.dietary-tag {
  display: inline-block;
  font-size: 11px;
}

.services-tabs {
  border-radius: 8px;
  overflow: hidden;
}

.services-tabs .btn-group {
  border-radius: 8px;
  overflow: hidden;
}

.services-tabs .btn {
  flex: 1;
  border-radius: 0;
  font-size: 13px;
  padding: 8px 12px;
}

.services-total {
  background: rgba(255, 255, 255, 0.05);
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 14px;
}

/* Boarding pass styles */
.boarding-pass {
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(20, 20, 35, 0.8));
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  position: relative;
  max-width: 300px;
  margin: 0 auto;
}

.boarding-pass-header {
  background: linear-gradient(90deg, var(--color-primary), var(--color-tertiary));
  padding: 15px;
  text-align: center;
  color: white;
}

.airline-name {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 2px;
}

.boarding-title {
  font-size: 12px;
  letter-spacing: 1px;
  opacity: 0.8;
}

.boarding-pass-body {
  padding: 15px;
}

.boarding-row {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
}

.boarding-col {
  flex: 1;
}

.boarding-label {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 2px;
}

.boarding-value {
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.boarding-pass-footer {
  padding: 15px;
  text-align: center;
  border-top: 1px dashed rgba(255, 255, 255, 0.2);
}

.barcode {
  background: transparent;
}

.boarding-ref {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
}

/* Loading spinner */
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: var(--color-primary);
  animation: spin 1s ease-in-out infinite;
}

/* Empty state */
.empty-state-icon {
  color: var(--color-primary);
  opacity: 0.7;
}

/* Pagination styles */
.pagination {
  display: flex;
  justify-content: center;
}

.pagination .page-item .page-link {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  margin: 0 5px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.pagination .page-item .page-link:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.pagination .page-item.active .page-link {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.pagination .page-item.disabled .page-link {
  background: rgba(255, 255, 255, 0.02);
  color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.05);
}

/* Cancel modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.cancel-modal {
  width: 90%;
  max-width: 400px;
}

.cancel-modal-content {
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(20, 20, 35, 0.95));
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: slideUp 0.4s ease;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes float {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(30px, 30px);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .flight-path {
    width: 80px;
  }

  .airport-code {
    font-size: 18px;
  }

  .boarding-pass {
    margin-top: 20px;
  }

  .ticket-status-badge {
    right: 10px;
    padding: 3px 10px;
    font-size: 10px;
  }

  .services-tabs .btn {
    font-size: 11px;
    padding: 6px 8px;
  }

  .services-tabs .btn svg {
    margin-right: 0 !important;
  }
}

/* Additional service styles */
.empty-service-icon {
  color: var(--color-primary);
  opacity: 0.7;
}

.service-tab-content {
  padding: 15px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.meal-card .service-card-icon {
  background: rgba(255, 193, 7, 0.1);
}

.baggage-card .service-card-icon {
  background: rgba(23, 162, 184, 0.1);
}

.comfort-card .service-card-icon {
  background: rgba(40, 167, 69, 0.1);
}

.btn-left {
  border-top-left-radius: 8px !important;
  border-bottom-left-radius: 8px !important;
}

.btn-right {
  border-top-right-radius: 8px !important;
  border-bottom-right-radius: 8px !important;
}

.ticket-status-badge.late {
  background: rgba(255, 193, 7, 0.2);
  color: var(--color-warning);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-top: none;
}

.ticket-status-badge.used {
  background: rgba(108, 117, 125, 0.2);
  color: #6c757d;
  border: 1px solid rgba(108, 117, 125, 0.3);
  border-top: none;
}

.ticket-status-badge.boarded {
  background: rgba(0, 201, 167, 0.2);
  color: var(--color-success);
  border: 1px solid rgba(0, 201, 167, 0.3);
  border-top: none;
}

.ticket-status-badge.checked_in {
  background: rgba(67, 203, 255, 0.2);
  color: var(--color-tertiary);
  border: 1px solid rgba(67, 203, 255, 0.3);
  border-top: none;
}
</style>