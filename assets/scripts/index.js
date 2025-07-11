import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap'
import { createApp } from 'vue'
import HomePage from './components/HomePage.vue'
import BookingsPage from './components/BokkingsPage.vue'
import '../styles/main.css'

const homeContainer = document.getElementById('app')
const bookingsContainer = document.getElementById('bookings')

if (homeContainer) {
    createApp(HomePage).mount('#app')
} else if (bookingsContainer) {
    createApp(BookingsPage).mount('#bookings')
}
