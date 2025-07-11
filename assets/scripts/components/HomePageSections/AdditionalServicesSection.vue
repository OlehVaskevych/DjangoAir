<template>
  <!-- Section 4: Additional Services -->
  <section
    id="services"
    class="min-vh-100 d-flex align-items-center justify-content-center position-relative"
    v-show="currentSection === 'services'"
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
            <h2 class="display-5 fw-bold text-gradient-alt">Enhance Your Journey</h2>
            <p class="text-white opacity-75">Select additional services to make your flight more comfortable</p>
          </div>

          <div class="card glass-card border-0 rounded-4">
            <div class="card-body p-4 p-md-5">
              <div class="row g-4">
                <!-- Services Selection -->
                <div class="col-lg-8">
                  <div class="services-container">
                    <!-- Meal Options -->
                    <div class="service-category mb-5">
                      <h3 class="fs-4 fw-semibold mb-3 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-cup-hot me-2 text-primary" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M.5 6a.5.5 0 0 0-.488.608l1.652 7.434A2.5 2.5 0 0 0 4.104 16h5.792a2.5 2.5 0 0 0 2.44-1.958l.131-.59a3 3 0 0 0 1.3-5.854l.221-.99A.5.5 0 0 0 13.5 6H.5ZM13 12.5a2.01 2.01 0 0 1-.316-.025l.867-3.898A2.001 2.001 0 0 1 13 12.5ZM2.64 13.825 1.123 7h11.754l-1.517 6.825A1.5 1.5 0 0 1 9.896 15H4.104a1.5 1.5 0 0 1-1.464-1.175Z"/>
                          <path d="m4.4.8-.003.004-.014.019a4.167 4.167 0 0 0-.204.31 2.327 2.327 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.31 3.31 0 0 1-.202.388 5.444 5.444 0 0 1-.253.382l-.018.025-.005.008-.002.002A.5.5 0 0 1 3.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 3.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 3 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 4.4.8Zm3 0-.003.004-.014.019a4.167 4.167 0 0 0-.204.31 2.327 2.327 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.31 3.31 0 0 1-.202.388 5.444 5.444 0 0 1-.253.382l-.018.025-.005.008-.002.002A.5.5 0 0 1 6.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 6.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 6 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 7.4.8Zm3 0-.003.004-.014.019a4.077 4.077 0 0 0-.204.31 2.337 2.337 0 0 0-.141.267c-.026.06-.034.092-.037.103v.004a.593.593 0 0 0 .091.248c.075.133.178.272.308.445l.01.012c.118.158.26.347.37.543.112.2.22.455.22.745 0 .188-.065.368-.119.494a3.198 3.198 0 0 1-.202.388 5.385 5.385 0 0 1-.252.382l-.019.025-.005.008-.002.002A.5.5 0 0 1 9.6 4.2l.003-.004.014-.019a4.149 4.149 0 0 0 .204-.31 2.06 2.06 0 0 0 .141-.267c.026-.06.034-.092.037-.103a.593.593 0 0 0-.09-.252A4.334 4.334 0 0 0 9.6 2.8l-.01-.012a5.099 5.099 0 0 1-.37-.543A1.53 1.53 0 0 1 9 1.5c0-.188.065-.368.119-.494.059-.138.134-.274.202-.388a5.446 5.446 0 0 1 .253-.382l.025-.035A.5.5 0 0 1 10.4.8Z"/>
                        </svg>
                        Meal Options
                      </h3>
                      <div class="row g-3">
                        <div class="col-md-6" v-for="(meal, index) in mealOptions" :key="`meal-${index}`">
                          <div
                            class="service-card p-3 rounded-4"
                            :class="{ 'selected': selectedServices.meals.includes(meal.id) }"
                            @click="toggleService('meals', meal.id, meal.price)"
                          >
                            <div class="d-flex justify-content-between align-items-start mb-2">
                              <h4 class="fs-5 mb-0 text-white">{{ meal.name }}</h4>
                              <span class="badge bg-primary rounded-pill">${{ meal.price.toFixed(2) }}</span>
                            </div>
                            <p class="small text-white-50 mb-2">{{ meal.description }}</p>
                            <div class="service-image mb-2">
                              <img :src="meal.image" alt="Meal image" class="img-fluid rounded-3">
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                              <div class="dietary-info small">
                                <span v-for="tag in meal.dietary" :key="tag" class="badge bg-secondary me-1">{{ tag }}</span>
                              </div>
                              <div class="selection-indicator">
                                <svg v-if="selectedServices.meals.includes(meal.id)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-check-circle-fill text-success" viewBox="0 0 16 16">
                                  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                                </svg>
                                <span v-else class="text-white-50 small">Select</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Baggage Options -->
                    <div class="service-category mb-5">
                      <h3 class="fs-4 fw-semibold mb-3 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-briefcase me-2 text-primary" viewBox="0 0 16 16">
                          <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l6.614 1.764a1.5 1.5 0 0 0 .772 0zM1.5 4h13a.5.5 0 0 1 .5.5v1.616L8.129 7.948a.5.5 0 0 1-.258 0L1 6.116V4.5a.5.5 0 0 1 .5-.5z"/>
                        </svg>
                        Extra Baggage
                      </h3>
                      <div class="row g-3">
                        <div class="col-md-6" v-for="(baggage, index) in baggageOptions" :key="`baggage-${index}`">
                          <div
                            class="service-card p-3 rounded-4"
                            :class="{ 'selected': selectedServices.baggage.includes(baggage.id) }"
                            @click="toggleService('baggage', baggage.id, baggage.price)"
                          >
                            <div class="d-flex justify-content-between align-items-start mb-2">
                              <h4 class="fs-5 mb-0 text-white">{{ baggage.name }}</h4>
                              <span class="badge bg-primary rounded-pill">${{ baggage.price.toFixed(2) }}</span>
                            </div>
                            <p class="small text-white-50 mb-2">{{ baggage.description }}</p>
                            <div class="d-flex justify-content-between align-items-center">
                              <div class="baggage-info">
                                <span class="badge bg-info me-1">{{ baggage.weight }} kg</span>
                              </div>
                              <div class="selection-indicator">
                                <svg v-if="selectedServices.baggage.includes(baggage.id)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-check-circle-fill text-success" viewBox="0 0 16 16">
                                  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                                </svg>
                                <span v-else class="text-white-50 small">Select</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Comfort Options -->
                    <div class="service-category">
                      <h3 class="fs-4 fw-semibold mb-3 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-stars me-2 text-primary" viewBox="0 0 16 16">
                          <path d="M7.657 6.247c.11-.33.576-.33.686 0l.645 1.937a2.89 2.89 0 0 0 1.829 1.828l1.936.645c.33.11.33.576 0 .686l-1.937.645a2.89 2.89 0 0 0-1.828 1.829l-.645 1.936a.361.361 0 0 1-.686 0l-.645-1.937a2.89 2.89 0 0 0-1.828-1.828l-1.937-.645a.361.361 0 0 1 0-.686l1.937-.645a2.89 2.89 0 0 0 1.828-1.828l.645-1.937zM3.794 1.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387A1.734 1.734 0 0 0 4.593 5.69l-.387 1.162a.217.217 0 0 1-.412 0L3.407 5.69A1.734 1.734 0 0 0 2.31 4.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387A1.734 1.734 0 0 0 3.407 2.31l.387-1.162zM10.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732L9.1 2.137a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L10.863.1z"/>
                        </svg>
                        Comfort Extras
                      </h3>
                      <div class="row g-3">
                        <div class="col-md-6" v-for="(comfort, index) in comfortOptions" :key="`comfort-${index}`">
                          <div
                            class="service-card p-3 rounded-4"
                            :class="{ 'selected': selectedServices.comfort.includes(comfort.id) }"
                            @click="toggleService('comfort', comfort.id, comfort.price)"
                          >
                            <div class="d-flex justify-content-between align-items-start mb-2">
                              <h4 class="fs-5 mb-0 text-white">{{ comfort.name }}</h4>
                              <span class="badge bg-primary rounded-pill">${{ comfort.price.toFixed(2) }}</span>
                            </div>
                            <p class="small text-white-50 mb-2">{{ comfort.description }}</p>
                            <div class="selection-indicator">
                              <svg v-if="selectedServices.comfort.includes(comfort.id)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-check-circle-fill text-success" viewBox="0 0 16 16">
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                              </svg>
                              <span v-else class="text-white-50 small">Select</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Services Summary -->
                <div class="col-lg-4">
                  <div class="card summary-card h-100 border-0 rounded-4">
                    <div class="card-body p-4">
                      <h3 class="fs-4 fw-semibold mb-4 text-white">Your Selections</h3>

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
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-white opacity-75">Selected Seats:</span>
                          <span class="fw-medium text-white">{{ selectedSeatsDisplay }}</span>
                        </div>
                      </div>

                      <hr class="my-4 opacity-25">

                      <!-- Selected Services Summary -->
                      <div class="mb-4">
                        <h4 class="fs-5 mb-3 text-white">Additional Services</h4>

                        <!-- Meals -->
                        <div v-if="selectedServices.meals.length > 0" class="service-summary-section mb-3">
                          <h5 class="fs-6 text-white-50">Meals</h5>
                          <div v-for="mealId in selectedServices.meals" :key="`meal-summary-${mealId}`" class="service-summary-item d-flex justify-content-between mb-2">
                            <span class="text-white">{{ getMealName(mealId) }}</span>
                            <span class="text-white">${{ getMealPrice(mealId).toFixed(2) }}</span>
                          </div>
                        </div>

                        <!-- Baggage -->
                        <div v-if="selectedServices.baggage.length > 0" class="service-summary-section mb-3">
                          <h5 class="fs-6 text-white-50">Extra Baggage</h5>
                          <div v-for="baggageId in selectedServices.baggage" :key="`baggage-summary-${baggageId}`" class="service-summary-item d-flex justify-content-between mb-2">
                            <span class="text-white">{{ getBaggageName(baggageId) }}</span>
                            <span class="text-white">${{ getBaggagePrice(baggageId).toFixed(2) }}</span>
                          </div>
                        </div>

                        <!-- Comfort -->
                        <div v-if="selectedServices.comfort.length > 0" class="service-summary-section mb-3">
                          <h5 class="fs-6 text-white-50">Comfort Extras</h5>
                          <div v-for="comfortId in selectedServices.comfort" :key="`comfort-summary-${comfortId}`" class="service-summary-item d-flex justify-content-between mb-2">
                            <span class="text-white">{{ getComfortName(comfortId) }}</span>
                            <span class="text-white">${{ getComfortPrice(comfortId).toFixed(2) }}</span>
                          </div>
                        </div>

                        <div v-if="!hasSelectedServices" class="text-center py-3">
                          <p class="text-white-50 mb-0">No additional services selected</p>
                        </div>
                      </div>

                      <hr class="my-4 opacity-25">

                      <!-- Price Summary -->
                      <div class="mb-4">
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-white opacity-75">Seats Total:</span>
                          <span class="text-white">${{ calculateSeatsTotal().toFixed(2) }}</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-white opacity-75">Services Total:</span>
                          <span class="text-white">${{ calculateServicesTotal().toFixed(2) }}</span>
                        </div>
                        <div class="d-flex justify-content-between fs-5 fw-bold mt-3">
                          <span class="text-white">Grand Total:</span>
                          <span class="text-glow">${{ calculateGrandTotal().toFixed(2) }}</span>
                        </div>
                      </div>

                      <div class="d-grid gap-2">
                        <button
                          @click="proceedToPayment"
                          class="btn btn-glow w-100 py-3 rounded-pill shadow"
                          :disabled="!hasSelectedServices"
                        >
                          <span class="fw-bold">Proceed to Payment</span>
                          <div class="btn-particles"></div>
                        </button>
                        <button
                          @click="skipServices"
                          class="btn btn-outline-light w-100 py-2 rounded-pill"
                          :disabled="!selectedSeats.length"
                        >
                          <span>Skip Additional Services</span>
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
    <div class="section-transition bottom-transition">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="rgba(26, 26, 46, 0.5)" fill-opacity="0.5" d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,224C672,245,768,267,864,261.3C960,256,1056,224,1152,208C1248,192,1344,192,1392,192L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    currentSection: {
      type: String,
      required: true
    },
    bookingDetails: {
      type: Object,
      required: true
    },
    selectedSeats: {
      type: Array,
      required: true
    },
    seatPrices: {
      type: Object,
      required: true,
    },
    selectedSeatsDisplay: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      // Додаткові послуги
      mealOptions: [],
      baggageOptions: [],
      selectedServices: {
        meals: [],
        baggage: [],
        comfort: []
      }
    };
  },

  computed: {
    /**
     * Checks if any services have been selected
     * @returns {boolean} True if at least one service is selected
     */
    hasSelectedServices() {
      return this.selectedServices.meals.length > 0 ||
             this.selectedServices.baggage.length > 0 ||
             this.selectedServices.comfort.length > 0;
    }
  },

  methods: {
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
     * Toggles selection of a service
     * @param {string} category - Service category (meals, baggage, comfort)
     * @param {string} id - Service ID
     * @param {number} price - Service price
     */
    toggleService(category, id, price) {
      const index = this.selectedServices[category].indexOf(id);
      if (index === -1) {
        // Add service
        this.selectedServices[category].push(id);
      } else {
        // Remove service
        this.selectedServices[category].splice(index, 1);
      }
    },

    /**
     * Gets meal name by ID
     * @param {string} id - Meal ID
     * @returns {string} Meal name
     */
    getMealName(id) {
      const meal = this.mealOptions.find(meal => meal.id === id);
      return meal ? meal.name : '';
    },

    /**
     * Gets meal price by ID
     * @param {string} id - Meal ID
     * @returns {number} Meal price
     */
    getMealPrice(id) {
      const meal = this.mealOptions.find(meal => meal.id === id);
      return meal ? meal.price : 0;
    },

    getMealPriceId(id) {
      const meal = this.mealOptions.find(meal => meal.id === id);
      return meal ? meal.price_id : '';
    },

    /**
     * Gets baggage name by ID
     * @param {string} id - Baggage ID
     * @returns {string} Baggage name
     */
    getBaggageName(id) {
      const baggage = this.baggageOptions.find(baggage => baggage.id === id);
      return baggage ? baggage.name : '';
    },

    /**
     * Gets baggage price by ID
     * @param {string} id - Baggage ID
     * @returns {number} Baggage price
     */
    getBaggagePrice(id) {
      const baggage = this.baggageOptions.find(baggage => baggage.id === id);
      return baggage ? baggage.price : 0;
    },

    getBaggagePriceId(id) {
      const baggage = this.baggageOptions.find(baggage => baggage.id === id);
      return baggage ? baggage.price_id : '';
    },

    /**
     * Gets comfort name by ID
     * @param {string} id - Comfort ID
     * @returns {string} Comfort name
     */
    getComfortName(id) {
      const comfort = this.comfortOptions.find(comfort => comfort.id === id);
      return comfort ? comfort.name : '';
    },

    /**
     * Gets comfort price by ID
     * @param {string} id - Comfort ID
     * @returns {number} Comfort price
     */
    getComfortPrice(id) {
      const comfort = this.comfortOptions.find(comfort => comfort.id === id);
      return comfort ? comfort.price : 0;
    },

    getComfortPriceId(id) {
      const comfort = this.comfortOptions.find(comfort => comfort.id === id);
      return comfort ? comfort.price_id : '';
    },

    /**
     * Calculates total price for seats
     * @returns {number} Total price for seats
     */
    calculateSeatsTotal() {
      return this.selectedSeats.reduce((total, seat) => {
        return total + this.getSeatPrice(seat.class);
      }, 0);
    },

    /**
     * Gets the price for a specific seat class
     * @param {string} seatClass - Class of the seat (first, business, economy)
     * @returns {number} Price of the seat based on its class
     */
    getSeatPrice(seatClass) {
      return this.seatPrices[seatClass] || this.seatPrices.economy;
    },

    /**
     * Calculates total price for additional services
     * @returns {number} Total price for services
     */
    calculateServicesTotal() {
      let total = 0;

      // Add meal prices
      this.selectedServices.meals.forEach(mealId => {
        total += this.getMealPrice(mealId);
      });

      // Add baggage prices
      this.selectedServices.baggage.forEach(baggageId => {
        total += this.getBaggagePrice(baggageId);
      });

      // Add comfort prices
      this.selectedServices.comfort.forEach(comfortId => {
        total += this.getComfortPrice(comfortId);
      });

      return total;
    },

    /**
     * Calculates grand total (seats + services)
     * @returns {number} Grand total price
     */
    calculateGrandTotal() {
      return this.calculateSeatsTotal() + this.calculateServicesTotal();
    },

    /**
     * Proceeds to payment with selected services
     */
    proceedToPayment() {
      // Prepare service details for backend
      const serviceDetails = {
        meals: this.selectedServices.meals.map(id => ({
          id,
          name: this.getMealName(id),
          price: this.getMealPrice(id),
          priceId: this.getMealPriceId(id),
        })),
        baggage: this.selectedServices.baggage.map(id => ({
          id,
          name: this.getBaggageName(id),
          price: this.getBaggagePrice(id),
          priceId: this.getBaggagePriceId(id),
        })),
        comfort: this.selectedServices.comfort.map(id => ({
          id,
          name: this.getComfortName(id),
          price: this.getComfortPrice(id),
          priceId: this.getComfortPriceId(id),
        }))
      };

      // Emit event to parent component with all booking data
      this.$emit('proceed-payment', {
        selectedServices: serviceDetails,
        servicesTotal: this.calculateServicesTotal()
      });
    },

    /**
     * Skips additional services and proceeds to payment
     */
    skipServices() {
      // Clear all selected services
      this.selectedServices = {
        meals: [],
        baggage: [],
        comfort: []
      };

      // Proceed to payment with only seat selections
      this.proceedToPayment();
    }
  },

  mounted() {
    fetch('/api/additional_services/')
        .then(response => response.json())
        .then(data => {
          this.mealOptions = data.meals;
          this.baggageOptions = data.baggage;
          this.comfortOptions = data.comfort;
        })
        .catch(error => {
          console.log('Failed to fetch additional services.', error);
        })
  }
};
</script>

<style scoped>
/* Service Cards */
.service-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.service-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.service-card.selected {
  background: rgba(108, 99, 255, 0.15);
  border: 1px solid var(--color-primary);
  box-shadow: 0 0 15px rgba(108, 99, 255, 0.3);
}

.service-card.selected:before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 30px 30px 0;
  border-color: transparent var(--color-primary) transparent transparent;
}

.service-image {
  height: 100px;
  overflow: hidden;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.2);
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-category {
  margin-bottom: 30px;
}

.service-summary-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 15px;
}

.service-summary-item {
  padding: 5px 0;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.1);
}

.service-summary-item:last-child {
  border-bottom: none;
}

/* Animations */
@keyframes pulse-border {
  0% {
    box-shadow: 0 0 0 0 rgba(108, 99, 255, 0.7);
  }
  70% {
    box-shadow: 0 0 0 5px rgba(108, 99, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(108, 99, 255, 0);
  }
}

.service-card.selected {
  animation: pulse-border 2s infinite;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .service-card {
    margin-bottom: 15px;
  }

  .service-image {
    height: 80px;
  }
}

/* Верхній перехід (зверху секції) */
.top-transition {
  top: 0;
}
</style>