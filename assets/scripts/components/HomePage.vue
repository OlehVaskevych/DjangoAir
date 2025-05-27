<template>
<div class="booking-app">

  <!-- Додайте обробники подій -->
  <AuthModels
    ref="authModels"
    v-if="!isAuthenticated"
    :currentSection="currentSection"
    @login-success="handleAuthSuccess"
    @register-success="handleAuthSuccess"
  />

  <!-- User Profile Button (показується тільки якщо користувач авторизований) -->
  <div v-if="isAuthenticated" class="user-profile-container">
    <button @click.stop="showUserProfile" class="user-profile-button">
      <span class="user-avatar">{{ userInitials }}</span>
    </button>

    <!-- Випадаюче меню профілю -->
    <div v-if="isProfileMenuOpen" class="profile-dropdown">
      <div class="profile-header">
        <span class="profile-name">{{ userData.name }}</span>
        <span class="profile-email">{{ userData.email }}</span>
      </div>
      <div class="profile-menu-items">
        <a href="/" class="profile-menu-item active">Home</a>
        <a href="/bookings" class="profile-menu-item">My Bookings</a>
        <a v-if="userData.role === 'gate_manager'" href="/staff_dashboard" class="profile-menu-item">Gate Manager Dashboard</a>
        <a v-else-if="userData.role === 'checkin_manager'" href="/staff_dashboard" class="profile-menu-item">Check-In Manager Dashboard</a>
        <a v-else-if="userData.role === 'supervisor'" href="/staff_dashboard" class="profile-menu-item">Supervisor Dashboard</a>
        <button @click="logout" class="profile-menu-item logout-button">Logout</button>
      </div>
    </div>
  </div>

  <!-- Auth Required Message -->
  <div v-if="showAuthRequiredMessage" class="auth-required-message">
    <div class="auth-required-content">
      <button @click="closeAuthRequiredMessage" class="close-button">&times;</button>
      <h3>Authentication Required</h3>
      <p>Please login or register to continue booking your flight.</p>
      <div class="auth-buttons">
        <button @click="openLoginModal" class="btn-login">Login</button>
        <button @click="openRegisterModal" class="btn-register">Register</button>
      </div>
    </div>
  </div>

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

  <!-- Section 1: Introduction -->
  <section
    id="intro"
    class="min-vh-100 d-flex align-items-center justify-content-center position-relative overflow-hidden"
    v-show="currentSection === 'intro'"
  >
    <!-- Airplane animation -->
    <div class="airplane-path">
      <div class="airplane-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" viewBox="0 0 16 16" style="transform: rotate(90deg)">
          <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
        </svg>
      </div>
      <div class="path-line"></div>
    </div>

    <div class="container py-5 z-index-2 position-relative">
      <div class="row justify-content-center">
        <div class="col-md-10 text-center">
          <div class="intro-content glass-card">
            <div class="logo-container mb-4">
              <div class="logo-circle">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="bi bi-airplane text-primary" viewBox="0 0 16 16">
                  <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
                </svg>
              </div>
            </div>
            <h1 class="display-3 fw-bold mb-4 text-gradient">DjangoAIR</h1>
            <p class="fs-4 mb-5 text-white">Experience the freedom of the skies with comfort and style. Your journey begins with us.</p>
            <button @click="showSection('booking')" class="btn btn-glow btn-lg px-5 py-3 rounded-pill shadow-lg">
              <span class="fw-bold">Book Your Flight</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Section transition element -->
    <div class="section-transition">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="rgba(26, 26, 46, 0.5)" fill-opacity="0.5" d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,224C672,245,768,267,864,261.3C960,256,1056,224,1152,208C1248,192,1344,192,1392,192L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
    </div>
  </section>

  <!-- Section 2: Booking Form -->
  <section
    id="booking"
    class="min-vh-100 d-flex align-items-center justify-content-center position-relative"
    v-show="currentSection === 'booking'"
  >
    <div class="section-transition top-transition">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="rgba(26, 26, 46, 0.5)" fill-opacity="0.5" d="M0,96L48,112C96,128,192,160,288,186.7C384,213,480,235,576,224C672,213,768,171,864,165.3C960,160,1056,192,1152,197.3C1248,203,1344,181,1392,170.7L1440,160L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
      </svg>
    </div>

    <div class="container py-5 z-index-2 position-relative">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="text-center mb-5">
            <h2 class="display-5 fw-bold text-gradient-alt">Book Your Flight</h2>
            <p class="text-white opacity-75">Select your destination, date, and number of passengers</p>
          </div>

          <div class="card glass-card border-0 rounded-4">
            <div class="card-body p-4 p-md-5">
              <div class="row g-4">
                <div class="col-md-4">
                  <div class="mb-3">
                    <label for="destination" class="form-label fw-medium text-white">Destination</label>
                    <div class="input-group input-group-glow">
                      <span class="input-group-text bg-transparent border-end-0">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-geo-alt text-primary" viewBox="0 0 16 16">
                          <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                          <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                        </svg>
                      </span>
                      <select id="destination" class="form-select form-control-lg bg-transparent border-start-0 text-white" v-model="bookingDetails.destination">
                        <option value="" selected disabled>Select destination</option>
                        <option v-for="city in destinations" :key="city" :value="city">{{ city }}</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div class="col-md-4">
                  <div class="mb-3">
                    <label for="date" class="form-label fw-medium text-white">Date</label>
                    <div class="input-group input-group-glow">
                      <span class="input-group-text bg-transparent border-end-0">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-calendar-event text-primary" viewBox="0 0 16 16">
                          <path d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"/>
                          <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                        </svg>
                      </span>
                      <select id="date" class="form-select form-control-lg bg-transparent border-start-0 text-white"
                             v-model="bookingDetails.date"
                             :disabled="!bookingDetails.destination"
                             :list="'available-dates'">
                        <option v-for="dateObj in availableDates" :key="dateObj.fullDate" :value="dateObj.fullDate">
                          {{ dateObj.displayDate }}
                        </option>
                      </select>
                    </div>
                    <!-- Список доступних дат -->
                    <datalist id="available-dates">
                      <option v-for="date in availableDates" :value="date" :key="date"></option>
                    </datalist>
                  </div>
                </div>

                <div class="col-md-4">
                  <div class="mb-3">
                    <label for="passengers" class="form-label fw-medium text-white">Passengers</label>
                    <div class="input-group input-group-glow">
                      <button @click="decrementPassengers" class="btn btn-outline-light" :disabled="bookingDetails.passengers <= 1">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-dash" viewBox="0 0 16 16">
                          <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                        </svg>
                      </button>
                      <input type="number" id="passengers" class="form-control form-control-lg text-center bg-transparent text-white" v-model="bookingDetails.passengers" min="1" max="10" readonly>
                      <button @click="incrementPassengers" class="btn btn-outline-light" :disabled="bookingDetails.passengers >= 10">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                          <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="text-center mt-5">
                <button
                  @click="proceedToSeatSelection"
                  class="btn btn-glow btn-lg px-5 py-3 rounded-pill shadow-lg"
                  :disabled="!isBookingFormValid"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-arrow-right me-2" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
                  </svg>
                  Select Seats
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section transition element -->
    <div class="section-transition section3-transition">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="rgba(26, 26, 46, 0.5)" fill-opacity="0.5" d="M0,96L48,112C96,128,192,160,288,186.7C384,213,480,235,576,224C672,213,768,171,864,165.3C960,160,1056,192,1152,197.3C1248,203,1344,181,1392,170.7L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
    </div>
  </section>

  <!-- Section 3: Seat Selection -->
  <section
    id="seats"
    class="min-vh-100 d-flex align-items-center justify-content-center position-relative"
    v-show="currentSection === 'seats'"
  >
    <div class="section-transition top-transition section3-transition">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="rgba(26, 26, 46, 0.5)" fill-opacity="0.5" d="M0,96L48,112C96,128,192,160,288,186.7C384,213,480,235,576,224C672,213,768,171,864,165.3C960,160,1056,192,1152,197.3C1248,203,1344,181,1392,170.7L1440,160L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
      </svg>
    </div>

    <div class="container py-5 z-index-2 position-relative">
      <div class="row justify-content-center">
        <div class="col-lg-11">
          <div class="text-center mb-4">
            <h2 class="display-5 fw-bold text-gradient-alt">Select Your Seats</h2>
            <p class="text-white opacity-75">Please select {{ bookingDetails.passengers }} seat(s) for your flight</p>
          </div>

          <div class="card glass-card border-0 rounded-4">
            <div class="card-body p-4 p-md-5">
              <div class="row g-4">
                <!-- Airplane Map -->
                <div class="col-lg-8">
                  <div class="airplane-container">
                    <!-- Airplane Header -->
                    <div class="d-flex justify-content-center mb-5">
                      <div class="airplane-cockpit"></div>
                    </div>

                    <!-- Seat Map -->
                    <div class="airplane-seats">
                      <!-- Використовуємо seatMap для відображення різних класів місць -->
                      <div v-for="(section, index) in seatSections" :key="index" class="cabin-section mb-4">
                        <div :class="`section-label ${section.labelClass} mb-3`">{{ section.name }}</div>

                        <div class="seat-row" v-for="row in section.rows" :key="`${section.class}-${row}`">
                          <div class="row-number">{{ row }}</div>

                          <!-- Left seats (A, B, C) -->
                          <div class="seats-group">
                            <div
                              v-for="seat in ['A', 'B', 'C']"
                              :key="`${row}${seat}`"
                              class="seat"
                              :class="{
                                [`${section.class}-seat`]: true,
                                'selected': isSelected(`${row}${seat}`),
                                'occupied': isOccupied(`${row}${seat}`),
                                'available': !isOccupied(`${row}${seat}`)
                              }"
                              @click="toggleSeat(`${row}${seat}`, section.class, section.priceId)"
                            >
                              {{ seat }}
                            </div>
                          </div>

                          <div class="aisle"></div>

                          <!-- Right seats (D, E, F) -->
                          <div class="seats-group">
                            <div
                              v-for="seat in ['D', 'E', 'F']"
                              :key="`${row}${seat}`"
                              class="seat"
                              :class="{
                                [`${section.class}-seat`]: true,
                                'selected': isSelected(`${row}${seat}`),
                                'occupied': isOccupied(`${row}${seat}`),
                                'available': !isOccupied(`${row}${seat}`)
                              }"
                              @click="toggleSeat(`${row}${seat}`, section.class, section.priceId)"
                            >
                              {{ seat }}
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Legend -->
                      <div class="seat-legend mt-4 d-flex justify-content-center flex-wrap gap-3">
                        <div class="d-flex align-items-center me-3">
                          <div class="seat-sample first-class-sample"></div>
                          <span class="ms-2 small text-white">First Class (${{ seatPrices.first.toFixed(2) }})</span>
                        </div>
                        <div class="d-flex align-items-center me-3">
                          <div class="seat-sample business-sample"></div>
                          <span class="ms-2 small text-white">Business (${{ seatPrices.business.toFixed(2) }})</span>
                        </div>
                        <div class="d-flex align-items-center me-3">
                          <div class="seat-sample economy-sample"></div>
                          <span class="ms-2 small text-white">Economy (${{ seatPrices.economy.toFixed(2) }})</span>
                        </div>
                        <div class="d-flex align-items-center me-3">
                          <div class="seat-sample selected"></div>
                          <span class="ms-2 small text-white">Selected</span>
                        </div>
                        <div class="d-flex align-items-center">
                          <div class="seat-sample occupied"></div>
                          <span class="ms-2 small text-white">Occupied</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Booking Summary -->
                <div class="col-lg-4">
                  <div class="card summary-card h-100 border-0 rounded-4">
                    <div class="card-body p-4">
                      <h3 class="fs-4 fw-semibold mb-4 text-white">Booking Summary</h3>

                      <div class="mb-4">
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-white opacity-75">Destination:</span>
                          <span class="fw-medium text-white">{{ bookingDetails.destination || '—' }}</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-white opacity-75">Date:</span>
                          <span class="fw-medium text-white">{{ formatDate(bookingDetails.date) }}</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-white opacity-75">Passengers:</span>
                          <span class="fw-medium text-white">{{ bookingDetails.passengers }}</span>
                        </div>
                      </div>

                      <hr class="my-4 opacity-25">

                      <div class="mb-4">
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-white opacity-75">Selected Seats:</span>
                          <span class="fw-medium text-white">{{ selectedSeatsDisplay }}</span>
                        </div>

                        <!-- Деталі вибраних місць -->
                        <div v-if="selectedSeats.length > 0" class="seat-details mt-3">
                          <div v-for="(seat, index) in selectedSeats" :key="index" class="seat-detail-item p-2 mb-2 rounded">
                            <div class="d-flex justify-content-between">
                              <span class="text-white">
                                <span :class="`seat-class-dot ${seat.class}`"></span>
                                Seat {{ seat.id }}
                              </span>
                              <span class="text-white">${{ getSeatPrice(seat.class).toFixed(2) }}</span>
                            </div>
                            <div class="seat-class-name small text-white-50">{{ getSeatClassName(seat.class) }}</div>
                          </div>
                        </div>
                      </div>

                      <hr class="my-4 opacity-25">

                      <div class="mb-4">
                        <div class="d-flex justify-content-between fs-5 fw-bold">
                          <span class="text-white">Total:</span>
                          <span class="text-glow">${{ calculateSeatsTotal().toFixed(2) }}</span>
                        </div>
                      </div>

                      <div class="d-grid gap-2">
                        <button
                          @click="proceedToServices"
                          class="btn btn-glow w-100 py-3 rounded-pill shadow"
                          :disabled="selectedSeats.length !== bookingDetails.passengers"
                        >
                          <span class="fw-bold">Proceed to Services</span>
                          <div class="btn-particles"></div>

                        </button>
                        <button
                          @click="submitPayment"
                          class="btn btn-outline-light w-100 py-2 rounded-pill"
                          :disabled="selectedSeats.length !== bookingDetails.passengers"
                        >
                          <span class="fw-bold">Skip Additional Services</span>
                          <div class="btn-particles"></div>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section transition element -->
    <div class="section-transition">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="rgba(26, 26, 46, 0.5)" fill-opacity="0.5" d="M0,160L48,170.7C96,181,192,203,288,192C384,181,480,139,576,138.7C672,139,768,181,864,197.3C960,213,1056,203,1152,181.3C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
    </div>
  </section>

  <!-- Додайте після секції seats -->
  <AdditionalServicesSection
    v-show="currentSection === 'services'"
    :currentSection="currentSection"
    :bookingDetails="bookingDetails"
    :selectedSeats="selectedSeats"
    :seatPrices="seatPrices"
    :selectedSeatsDisplay="selectedSeatsDisplay"
    @get-seat-price="getSeatPrice"
    @proceed-payment="handleServiceSelection"
  />

  <!-- Success Modal -->
  <div class="modal fade" id="successModal" tabindex="-1" aria-labelledby="successModalLabel" aria-hidden="true" ref="successModal">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content glass-card rounded-4 shadow border-0">
        <div class="modal-body p-5 text-center">
          <div class="success-animation mb-4">
            <div class="checkmark-circle">
              <div class="checkmark draw"></div>
            </div>
          </div>
          <h3 class="fs-2 fw-bold mb-3 text-gradient">Booking Successful!</h3>
          <p class="text-white mb-4">Your booking has been confirmed. A confirmation email has been sent to your email address.</p>
          <button
            type="button"
            class="btn btn-glow btn-lg px-5 py-3 rounded-pill shadow"
            data-bs-dismiss="modal"
            @click="resetBooking"
          >
            Book Another Flight
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import AuthModels from './HomePageSections/Register.vue';
import AdditionalServicesSection from "./HomePageSections/AdditionalServicesSection.vue";
import { emitter, EventTypes } from "@/scripts/eventBus";

// Declare the variables if they are not defined globally
const UNIQUE_CITIES_FROM_SERVER = window.UNIQUE_CITIES_FROM_SERVER || [];
const FLIGHT_DATES_FROM_SERVER = window.FLIGHT_DATES_FROM_SERVER || {};

console.log(UNIQUE_CITIES_FROM_SERVER);
console.log(FLIGHT_DATES_FROM_SERVER);

export default {
  components: { AuthModels, AdditionalServicesSection },

  data() {
    const today = new Date();
    const minDate = today.toISOString().split('T')[0];

    return {
      seatMap: [
        { row: 1, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'first', stripe_price_id: 'price_1RP0zFQMzydK9SUptZsV3qKC' },
        { row: 2, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'first', stripe_price_id: 'price_1RP0zFQMzydK9SUptZsV3qKC' },
        { row: 3, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'business', stripe_price_id: 'price_1RP0yyQMzydK9SUpQVDc8Xlz' },
        { row: 4, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'business', stripe_price_id: 'price_1RP0yyQMzydK9SUpQVDc8Xlz' },
        { row: 5, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'economy', stripe_price_id: 'price_1RP0yYQMzydK9SUprJfIiJYw' },
        { row: 6, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'economy', stripe_price_id: 'price_1RP0yYQMzydK9SUprJfIiJYw' },
        { row: 7, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'economy', stripe_price_id: 'price_1RP0yYQMzydK9SUprJfIiJYw' },
        { row: 8, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'economy', stripe_price_id: 'price_1RP0yYQMzydK9SUprJfIiJYw' },
        { row: 9, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'economy', stripe_price_id: 'price_1RP0yYQMzydK9SUprJfIiJYw' },
        { row: 10, seats: ['A', 'B', 'C', 'D', 'E', 'F'], class: 'economy', stripe_price_id: 'price_1RP0yYQMzydK9SUprJfIiJYw' }
      ],
      seatPrices: {
        first: 250,
        business: 150,
        economy: 75,
      },
      modal: null,
      destinations: UNIQUE_CITIES_FROM_SERVER,
      allFlights: FLIGHT_DATES_FROM_SERVER,
      currentSection: 'intro',
      bookingDetails: {
        flightId: null,
        destination: '',
        date: null,
        passengers: 1
      },
      selectedServices: {
        meals: [],
        baggage: [],
        comfort: []
      },
      availableDates: [],
      selectedSeats: [],
      occupiedSeats: [],
      seatPrice: 149.99,
      minDate: minDate,
      isProfileMenuOpen: false,
      showAuthRequiredMessage: false,

      // Authentication state and user data
      isAuthenticated: false,
      userData: {
        name: '',
        email: '',
        id: null,
        role: 'passenger'
      }
    };
  },
  created() {
    emitter.on(EventTypes.AUTH.LOGIN_SUCCESS, (userData) => {
      this.handleAuthSuccess(userData);
    });

    emitter.on(EventTypes.AUTH.REGISTER_SUCCESS, (userData) => {
      this.handleAuthSuccess(userData);
    });
  },
  computed: {
    /**
     * Validates if the booking form is filled correctly
     * Checks if destination is selected, date is chosen, and at least one passenger is specified
     * @returns {boolean} True if all required fields are filled, false otherwise
     */
    isBookingFormValid() {
      return this.bookingDetails.destination &&
             this.bookingDetails.date &&
             this.bookingDetails.passengers > 0;
    },

    /**
     * Generates user initials from the user's name for the avatar display
     * Takes the first letter of each word in the name (up to 2 letters)
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
     * Groups seats by class for display on the seat map
     * Organizes rows into sections (First Class, Business Class, Economy)
     * @returns {Array} Array of section objects with name, class, labelClass, and rows properties
     */
    seatSections() {
      const sections = [
        {
          name: 'First Class',
          class: 'first-class',
          labelClass: 'first-class-label',
          rows: [1, 2],
          priceId: 'price_1RP0zFQMzydK9SUptZsV3qKC',
        },
        {
          name: 'Business Class',
          class: 'business',
          labelClass: 'business-class-label',
          rows: [3, 4],
          priceId: 'price_1RP0yyQMzydK9SUpQVDc8Xlz'
        },
        {
          name: 'Economy',
          class: 'economy',
          labelClass: 'economy-label',
          rows: [5, 6, 7, 8, 9, 10],
          priceId: 'price_1RP0yYQMzydK9SUprJfIiJYw'
        }
      ];

      return sections;
    },

    /**
     * Formats selected seats for display in the booking summary
     * Joins seat IDs with commas or returns 'None' if no seats are selected
     * @returns {string} Comma-separated list of seat IDs or 'None'
     */
    selectedSeatsDisplay() {
      if (!this.selectedSeats.length) return 'None';
      return this.selectedSeats.map(seat => seat.id).join(', ');
    }
  },

  methods: {

    /**
     * Toggles the user profile dropdown menu visibility
     * Inverts the current state of isProfileMenuOpen
     */
    showUserProfile() {
      this.isProfileMenuOpen = !this.isProfileMenuOpen;
    },

    /**
     * Closes the profile menu when clicking outside of it
     * Checks if the click event target is not within the profile container
     * @param {Event} event - The click event object
     */
    closeProfileMenu(event) {
      if (this.isProfileMenuOpen && !event.target.closest('.user-profile-container')) {
        this.isProfileMenuOpen = false;
      }
    },

    /**
     * Handles navigation to booking section with authentication check
     * If user is authenticated, shows booking section
     * Otherwise, displays authentication required message
     */
    proceedToBooking() {
      if (this.isAuthenticated) {
        this.showSection('booking');
      } else {
        this.attemptedSection = 'booking';
        this.showAuthRequiredMessage = true;
      }
    },

    /**
     * Handles navigation to seat selection after booking form completion
     * Validates booking form, checks authentication, and resets selected seats
     * Shows authentication required message for unauthenticated users
     */
    proceedToSeatSelection() {
      if (this.isBookingFormValid) {
        if (this.isAuthenticated) {
          this.selectedSeats = [];
          this.showSection('seats');
        } else {
          this.attemptedSection = 'seats';
          this.showAuthRequiredMessage = true;
        }
      }
    },

    /**
     * Proceeds to services selection after seat selection
     */
    proceedToServices() {
      if (this.selectedSeats.length === this.bookingDetails.passengers) {
        this.showSection('services');
      } else {
        console.error('Please select all required seats first');
      }
    },

    /**
     * Обробляє успішну авторизацію або реєстрацію
     * @param {Object} userData - Дані користувача
     */
    handleAuthSuccess(userData) {
      this.isAuthenticated = true;

      if (userData) {
        this.userData = userData;
      }

      // Оновлюємо інтерфейс відповідно до стану авторизації
      // Наприклад, показуємо захищені секції або оновлюємо меню

      // Якщо користувач намагався перейти до захищеної секції
      if (this.attemptedSection) {
        this.showSection(this.attemptedSection);
        this.attemptedSection = null;
      }
    },

    /**
     * Handles user logout process
     * Clears authentication state, user data, and localStorage
     * Makes a logout request to the server
     * Redirects to the intro section
     */
    async logout() {
      try {
        const csrfToken = this.getCookie('csrftoken');
        if (!csrfToken) {
          console.error('CSRF token not found!');
          return;
        }
    
        const response = await fetch(`/auth/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'same-origin', // дуже важливо для куків
        });

        // Якщо сервер не повертає JSON, це викличе помилку
        const success = await response.json();

        if (success) {
          this.isAuthenticated = false;
          this.userData = { name: '', email: '', id: null, role: 'passenger' };
          this.isProfileMenuOpen = false;

          localStorage.removeItem('isAuthenticated');
          localStorage.removeItem('userData');

          this.showSection('intro');
        } else {
          console.error('Logout failed:', success);
        }
      } catch (error) {
        console.error('Request error:', error);
      }
    },

    /**
     * Closes the authentication required message
     * Resets the attempted section navigation
     */
    closeAuthRequiredMessage() {
      this.showAuthRequiredMessage = false;
      this.attemptedSection = null;
    },

    /**
     * Formats date string for display in the UI
     * Converts ISO date string to localized format with weekday, month, day, and year
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
     * Increases the number of passengers in the booking
     * Limits the maximum number of passengers to 10
     */
    incrementPassengers() {
      if (this.bookingDetails.passengers < 10) {
        this.bookingDetails.passengers++;
      }
    },

    /**
     * Decreases the number of passengers in the booking
     * Ensures at least 1 passenger remains selected
     */
    decrementPassengers() {
      if (this.bookingDetails.passengers > 1) {
        this.bookingDetails.passengers--;
      }
    },

    /**
     * Checks if a specific seat is already occupied
     * @param {string} seat - Seat ID to check (e.g., "1A", "2B")
     * @returns {boolean} True if the seat is in the occupiedSeats array, false otherwise
     */
    isOccupied(seat) {
      return this.occupiedSeats.includes(seat);
    },

    /**
     * Retrieves the price for a specific seat class
     * Falls back to economy price if the class is not found
     * @param {string} seatClass - Class of the seat (first, business, economy)
     * @returns {number} Price of the seat based on its class
     */
    getSeatPrice(seatClass) {
      return this.seatPrices[seatClass] || this.seatPrices.economy;
    },

    /**
     * Gets the display name for a seat class
     * Converts internal class name to user-friendly display name
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
     * Handles seat selection and deselection
     * Manages the selection state based on various conditions:
     * - Prevents selecting occupied seats
     * - Toggles selection state for already selected seats
     * - Prevents selecting more seats than passengers
     * - Sorts selected seats by row and letter for consistent display
     *
     * @param {string} seatId - ID of the seat being toggled (e.g., "1A", "2B")
     * @param {string} seatClass - Class of the seat (first-class, business, economy)
     * @param priceId
     */
    toggleSeat(seatId, seatClass, priceId) {
      // Prevent selecting occupied seats
      if (this.isOccupied(seatId)) return;

      // Find index of seat if already selected
      const existingIndex = this.selectedSeats.findIndex(seat => seat.id === seatId);

      // If seat is already selected, remove it
      if (existingIndex !== -1) {
        this.selectedSeats.splice(existingIndex, 1);
        return;
      }

      // Prevent selecting more seats than passengers
      if (this.selectedSeats.length >= this.bookingDetails.passengers) {
        return;
      }

      // Add new seat with appropriate class
      this.selectedSeats.push({
        id: seatId,
        class: seatClass.includes('first') ? 'first' :
               seatClass.includes('business') ? 'business' : 'economy',
        priceId: priceId,
      });

      // Sort seats by row number and then by letter
      this.selectedSeats.sort((a, b) => {
        // First compare row numbers
        const rowA = parseInt(a.id.match(/\d+/)[0]);
        const rowB = parseInt(b.id.match(/\d+/)[0]);

        if (rowA !== rowB) {
          return rowA - rowB;
        }

        // If rows are the same, compare letters
        return a.id.localeCompare(b.id);
      });
    },

    /**
     * Checks if a specific seat is currently selected
     * @param {string} seatId - ID of the seat to check (e.g., "1A", "2B")
     * @returns {boolean} True if the seat is in the selectedSeats array, false otherwise
     */
    isSelected(seatId) {
      return this.selectedSeats.some(seat => seat.id === seatId);
    },

    openLoginModal() {
      this.showAuthRequiredMessage = false;
      emitter.emit(EventTypes.AUTH.OPEN_LOGIN_MODAL);
    },

    /**
     * Opens the registration modal dialog
     * Closes the authentication required message first
     * Attempts to call the openRegisterModal method on the authModals component
     */
    openRegisterModal() {
      this.showAuthRequiredMessage = false;
      emitter.emit(EventTypes.AUTH.OPEN_REGISTER_MODAL);
    },

    /**
     * Navigates to a specific section with authentication check
     * Prevents access to protected sections (booking, seats, payment) for unauthenticated users
     * Smoothly scrolls to the target section
     *
     * @param {string} section - Section ID to navigate to (intro, booking, seats, payment)
     */
    showSection(section) {
      // Check authentication for protected sections
      if ((section === 'booking' || section === 'seats' || section === 'payment') && !this.isAuthenticated) {
        this.attemptedSection = section;
        this.showAuthRequiredMessage = true;
        return;
      }

      this.currentSection = section;
      // Smooth scroll to the section after a short delay
      setTimeout(() => {
        const element = document.getElementById(section);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    },



    /**
     * Submits payment information to the server
     * Validates authentication and seat selection
     * Prepares seat details and total amount for the payment request
     * Redirects to the payment URL returned by the server
     *
     * @async
     * @returns {Promise<void>}
     */
    async submitPayment() {
      // Check authentication
      if (!this.isAuthenticated) {
        this.attemptedSection = 'payment';
        this.showAuthRequiredMessage = true;
        return;
      }

      // Validate seat selection
      if (this.selectedSeats.length !== this.bookingDetails.passengers) {
        console.error('Choose correct quantity of passengers!');
        return;
      }

      // Prepare detailed information about selected seats
      const seatDetails = this.selectedSeats.map(seat => ({
        id: seat.id,
        class: seat.class,
        price: this.getSeatPrice(seat.class),
        priceId: seat.priceId,
      }));

      // Calculate total amount in cents for payment processing
      const totalAmount = Math.round(this.calculateSeatsTotal() * 100);

      try {
        // Send payment request to server
        const response = await fetch(`/create-checkout-session/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'),
          },
          body: JSON.stringify({
            flightId: this.bookingDetails.flightId,
            destination: this.bookingDetails.destination,
            date: this.bookingDetails.date,
            seats: this.selectedSeats.length,
            selectedSeats: seatDetails,
            totalAmount: totalAmount,
            selectedServices: this.selectedServices,
          })
        });

        const data = await response.json();

        // Redirect to payment URL if available
        if (data.url) {
          window.location.href = data.url;
        } else {
          console.error('Error');
        }
      } catch (error) {
        console.error('Request error:', error);
      }
    },

    /**
     * Resets the booking form to initial values
     * Clears destination, resets date to minimum date, sets passengers to 1
     * Clears selected seats and payment details
     * Navigates back to the booking section
     * Hides any open modals
     */
    resetBooking() {
      this.bookingDetails = {
        destination: '',
        date: this.minDate,
        passengers: 1
      };
      this.selectedSeats = [];
      this.paymentDetails = {
        cardholderName: '',
        cardNumber: '',
        expiryDate: '',
        cvv: '',
        billingAddress: '',
        termsAccepted: false
      };

      this.showSection('booking');
      if (this.modal) {
        this.modal.hide();
      }
    },

    /**
     * Checks user authentication status from localStorage on page load
     * Attempts to parse and restore user data from localStorage
     * Handles errors in case of invalid stored data
     */
    checkAuthentication() {
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
          localStorage.removeItem('isAuthenticated');
          localStorage.removeItem('userData');
        }
      }
    },
    /**
     * Handles service selection from the AdditionalServicesSection component
     * @param {Object} data - Selected services data
     */
    handleServiceSelection(data) {
      this.selectedServices = data.selectedServices;
      this.submitPayment();
    },


    /**
     * Calculates the total price of all selected seats
     * Sums up the prices of each selected seat based on its class
     * @returns {number} Total price of all selected seats
     */
    calculateSeatsTotal() {
      return this.selectedSeats.reduce((total, seat) => {
        return total + this.getSeatPrice(seat.class);
      }, 0);
    },

    /**
     * Calculates total price for additional services
     * @returns {number} Total price for services
     */
    calculateServicesTotal() {
      // Якщо немає вибраних послуг, повертаємо 0
      if (!this.selectedServices ||
          (!this.selectedServices.meals.length &&
           !this.selectedServices.baggage.length &&
           !this.selectedServices.comfort.length)) {
        return 0;
      }

      let total = 0;

      // Додаємо ціни за їжу
      if (this.selectedServices.meals) {
        this.selectedServices.meals.forEach(meal => {
          total += meal.price;
        });
      }

      // Додаємо ціни за багаж
      if (this.selectedServices.baggage) {
        this.selectedServices.baggage.forEach(baggage => {
          total += baggage.price;
        });
      }

      // Додаємо ціни за комфорт
      if (this.selectedServices.comfort) {
        this.selectedServices.comfort.forEach(comfort => {
          total += comfort.price;
        });
      }

      return total;
    },

    /**
     * Calculates the grand total including seats and services
     * @returns {number} Total price
     */
    calculateGrandTotal() {
      return this.calculateSeatsTotal() + this.calculateServicesTotal();
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

  watch: {
    /**
     * Watches for changes in the selected destination
     * Updates available flight dates based on the selected city
     * Formats dates for display in the UI
     * @param {string} newCity - The newly selected destination city
     */
    'bookingDetails.destination'(newCity) {
      if (newCity && this.allFlights[newCity]) {
        this.availableDates = this.allFlights[newCity].map(flight => ({
          fullDate: flight.date,
          displayDate: flight.time,
        }));
      } else {
        this.availableDates = [];
      }
    },

    /**
     * Watches for changes in the selected date
     * Updates occupied seats based on the selected date and destination
     * Logs errors if the selection is invalid or data is not available
     * @param {string} newDate - The newly selected date
     */
    'bookingDetails.date'(newDate) {
      const citySelected = this.bookingDetails.destination;
      const dateSelected = this.bookingDetails.date;
      const cityIsSelected = citySelected && citySelected !== '';
      const dateIsSelected = dateSelected && dateSelected !== '';

      if (cityIsSelected && dateIsSelected) {
        const selectedFlight = this.allFlights[citySelected].find(flight => flight.date === dateSelected);

        if (selectedFlight) {
          this.occupiedSeats = selectedFlight.taken;
          this.bookingDetails.flightId = selectedFlight.flight_id;
        } else {
          console.log('Error!');
        }
      } else {
        console.log('Error!');
      }
    }
  },

  mounted() {
    /**
     * Component mounted lifecycle hook
     * Fetches current user data from the server
     * Checks authentication status from localStorage
     * Initializes Bootstrap modal for success message
     * Sets up click event listener for closing the profile menu
     */
    fetch('/api/current_user/')
      .then(response => response.json())
      .then(data => {
        this.isAuthenticated = data.isAuthenticated;
        this.userData = {
          name: data.user.name,
          email: data.user.email,
          id: data.user.id,
          role: data.user.role,
        };
      })
      .catch(error => {
        console.error('Failed to fetch user data:', error);
        this.isAuthenticated = false;
        this.userData = {
          id: null,
          username: '',
          email: '',
          first_name: '',
          role: 'passenger'
        };
      });

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
     * Removes the click event listener to prevent memory leaks
     */
    document.removeEventListener('click', this.closeProfileMenu);
  }
};
</script>