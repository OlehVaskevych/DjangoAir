import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap'
import { createApp } from 'vue'
import HomePage from './components/HomePage.vue'
import BookingsPage from './components/BokkingsPage.vue'
import GateManagerPage from "./components/GateManagerPage.vue";
import CheckInManagerPage from "./components/CheckInManagerPage.vue";
import SupervisorPage from "./components/SupervisorPage.vue";
import '../styles/main.css'

const homeContainer = document.getElementById('app')
const bookingsContainer = document.getElementById('bookings')
const gateManagerContainer = document.getElementById('gate-manager')
const checkInManagerContainer = document.getElementById('check-in-manager')
const supervisorContainer = document.getElementById('supervisor')

if (homeContainer) {
    createApp(HomePage).mount('#app')
} else if (bookingsContainer) {
    createApp(BookingsPage).mount('#bookings')
} else if (gateManagerContainer) {
    createApp(GateManagerPage).mount('#gate-manager')
} else if (checkInManagerContainer) {
    createApp(CheckInManagerPage).mount('#check-in-manager')
} else if (supervisorContainer) {
    createApp(SupervisorPage).mount('#supervisor')
}
