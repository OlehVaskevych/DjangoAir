<template>
  <div>
    <!-- Прихований контейнер для рендерингу квитка -->
    <div class="hidden-ticket-container" ref="hiddenTicketContainer" style="display: none;">
      <div id="ticket-template" class="ticket-container" ref="ticketTemplate">
        <div class="ticket">
          <div class="ticket-header">
            <div class="logo">
              <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-airplane" viewBox="0 0 16 16">
                <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
              </svg>
              <span>DjangoAIR</span>
            </div>
            <div class="ticket-type">
              <span>Boarding Pass</span>
            </div>
          </div>

          <div class="ticket-body">
            <div class="flight-info">
              <div class="flight-route">
                <div class="departure">
                  <div class="city-code">{{ ticket.departureCode }}</div>
                  <div class="city-name">{{ ticket.departureCity }}</div>
                </div>

                <div class="flight-path">
                  <div class="plane-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-airplane" viewBox="0 0 16 16">
                      <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
                    </svg>
                  </div>
                  <div class="flight-line"></div>
                </div>

                <div class="arrival">
                  <div class="city-code">{{ ticket.arrivalCode }}</div>
                  <div class="city-name">{{ ticket.destination }}</div>
                </div>
              </div>

              <div class="flight-details">
                <div class="detail-item">
                  <div class="label">Flight</div>
                  <div class="value">{{ ticket.flightNumber }}</div>
                </div>
                <div class="detail-item">
                  <div class="label">Date</div>
                  <div class="value">{{ formatDate(ticket.date) }}</div>
                </div>
                <div class="detail-item">
                  <div class="label">Departure</div>
                  <div class="value">{{ ticket.departureTime }}</div>
                </div>
                <div class="detail-item">
                  <div class="label">Arrival</div>
                  <div class="value">{{ ticket.arrivalTime }}</div>
                </div>
              </div>
            </div>

            <div class="passenger-info">
              <div class="detail-item">
                <div class="label">Passenger</div>
                <div class="value">{{ ticket.passengerName }}</div>
              </div>
              <div class="detail-item">
                <div class="label">Passenger ID</div>
                <div class="value">{{ ticket.passengerId }}</div>
              </div>
              <div class="detail-item">
                <div class="label">Seat</div>
                <div class="value">{{ ticket.seats[0]?.id || 'N/A' }}</div>
              </div>
              <div class="detail-item">
                <div class="label">Class</div>
                <div class="value">{{ getSeatClassName(ticket.seats[0]?.class) }}</div>
              </div>
              <div class="detail-item">
                <div class="label">Gate</div>
                <div class="value">{{ ticket.gate }}</div>
              </div>
              <div class="detail-item">
                <div class="label">Boarding</div>
                <div class="value">{{ ticket.boardingTime }}</div>
              </div>
            </div>

            <div class="barcode-section">
              <div class="barcode" ref="barcodeContainer"></div>
              <div class="booking-reference">
                Booking Ref: {{ ticket.bookingReference }}
              </div>
            </div>
          </div>

          <div class="ticket-footer">
            <p>Thank you for choosing DjangoAIR. We wish you a pleasant flight!</p>
            <p class="small">This is an electronic ticket. Please present this document along with a photo ID at the check-in counter.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import html2pdf from 'html2pdf.js';
import JsBarcode from 'jsbarcode';

export default {
  name: 'FlightTicketButton',
  props: {
    ticket: {
      type: Object,
      required: true
    }
  },
  mounted() {
    // Генеруємо штрих-код для квитка
    this.$nextTick(() => {
      if (this.ticket.bookingReference && this.$refs.barcodeContainer) {
        JsBarcode(this.$refs.barcodeContainer, this.ticket.bookingReference, {
          format: "CODE128",
          lineColor: "#6c63ff",
          width: 2,
          height: 50,
          displayValue: false
        });
      }
    });
  },
  methods: {
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
    getSeatClassName(seatClass) {
      switch(seatClass) {
        case 'first': return 'First Class';
        case 'business': return 'Business Class';
        case 'economy': return 'Economy';
        default: return 'Economy';
      }
    },
    async generatePDF() {
      try {
        // Чекаємо, щоб DOM повністю оновився
        await this.$nextTick();

        // Отримуємо елемент шаблону квитка
        const element = this.$refs.ticketTemplate;

        // Налаштування для PDF
        const options = {
          margin: 10,
          filename: `ticket-${this.ticket.flightNumber}-${this.ticket.bookingReference}.pdf`,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 2, useCORS: true },
          jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };

        // Генеруємо PDF
        await html2pdf().from(element).set(options).save();

        return true;
      } catch (error) {
        console.error('Error generating PDF:', error);
        return false;
      }
    }
  }
};
</script>

<style scoped>
.ticket-container {
  font-family: 'Arial', sans-serif;
  width: 800px;
  margin: 0 auto;
  background-color: white;
  color: #1a1a2e;
}

.ticket {
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  background: white;
}

.ticket-header {
  background: linear-gradient(135deg, #6c63ff, #43cbff);
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
}

.logo svg {
  margin-right: 10px;
}

.ticket-type {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 5px 15px;
  border-radius: 20px;
  font-weight: bold;
}

.ticket-body {
  padding: 30px;
}

.flight-info {
  margin-bottom: 30px;
}

.flight-route {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.departure, .arrival {
  text-align: center;
  flex: 1;
}

.city-code {
  font-size: 36px;
  font-weight: bold;
  color: #1a1a2e;
}

.city-name {
  font-size: 16px;
  color: #666;
}

.flight-path {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 2;
  position: relative;
}

.plane-icon {
  background-color: #6c63ff;
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.flight-line {
  height: 2px;
  background-color: #ddd;
  width: 100%;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.flight-details {
  display: flex;
  justify-content: space-between;
  background-color: #f0f0f0;
  padding: 15px;
  border-radius: 8px;
}

.passenger-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f0f0f0;
  border-radius: 8px;
}

.passenger-info .detail-item {
  width: 30%;
  margin-bottom: 10px;
}

.detail-item {
  text-align: center;
}

.label {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.value {
  font-size: 16px;
  font-weight: bold;
  color: #1a1a2e;
}

.barcode-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.barcode {
  margin-bottom: 10px;
  height: 50px;
}

.booking-reference {
  font-size: 14px;
  font-weight: bold;
}

.ticket-footer {
  background-color: #f0f0f0;
  padding: 15px;
  text-align: center;
  font-size: 14px;
  color: #666;
  border-top: 1px dashed #ddd;
}

.small {
  font-size: 12px;
  margin-top: 5px;
}

/* Стилі для друку */
@media print {
  .ticket-container {
    width: 100%;
    background-color: white;
  }

  .ticket {
    box-shadow: none;
    border: 1px solid #ddd;
  }
}
</style>