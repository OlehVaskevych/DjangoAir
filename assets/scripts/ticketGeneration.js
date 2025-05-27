import html2pdf from 'html2pdf.js';
import JsBarcode from 'jsbarcode';

export default {
  async generateTicketPDF(ticket) {
    try {
      // Створюємо тимчасовий контейнер для рендерингу квитка
      const container = document.createElement('div');
      container.style.position = 'absolute';
      container.style.left = '-9999px';
      container.style.top = '-9999px';
      document.body.appendChild(container);

      // Створюємо HTML для квитка
      container.innerHTML = `
        <div id="ticket-template" class="ticket-container" style="font-family: Arial, sans-serif; width: 800px; margin: 0; padding: 0; background-color: white; color: #1a1a2e;">
          <div class="ticket" style="overflow: hidden; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); background: white; margin: 0; padding: 0">
            <div class="ticket-header" style="background: linear-gradient(135deg, #6c63ff, #43cbff); color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
              <div class="logo" style="display: flex; align-items: center; font-size: 24px; font-weight: bold;">
                <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 10px;">
                  <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
                </svg>
                <span>DjangoAIR</span>
              </div>
              <div class="ticket-type" style="background-color: rgba(255, 255, 255, 0.2); padding: 5px 15px; border-radius: 20px; font-weight: bold;">
                <span>Boarding Pass</span>
              </div>
            </div>
            
            <div class="ticket-body" style="padding: 30px;">
              <div class="flight-info" style="margin-bottom: 30px;">
                <div class="flight-route" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                  <div class="departure" style="text-align: center; flex: 1;">
                    <div class="city-code" style="font-size: 36px; font-weight: bold; color: #1a1a2e;">${ticket.departureCode}</div>
                    <div class="city-name" style="font-size: 16px; color: #666;">${ticket.departureCity}</div>
                  </div>
                  
                  <div class="flight-path" style="display: flex; flex-direction: column; align-items: center; flex: 2; position: relative;">
                    <div class="plane-icon" style="background-color: #6c63ff; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; z-index: 2; transform: rotateZ(90deg)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16" style="">
                        <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Z"/>
                      </svg>
                    </div>
                    <div class="flight-line" style="height: 2px; background-color: #ddd; width: 100%; position: absolute; top: 50%; transform: translateY(-50%);"></div>
                  </div>
                  
                  <div class="arrival" style="text-align: center; flex: 1;">
                    <div class="city-code" style="font-size: 36px; font-weight: bold; color: #1a1a2e;">${ticket.arrivalCode}</div>
                    <div class="city-name" style="font-size: 16px; color: #666;">${ticket.destination}</div>
                  </div>
                </div>
                
                <div class="flight-details" style="display: flex; justify-content: space-between; background-color: #f0f0f0; padding: 15px; border-radius: 8px;">
                  <div class="detail-item" style="text-align: center;">
                    <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Flight</div>
                    <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.flightNumber}</div>
                  </div>
                  <div class="detail-item" style="text-align: center;">
                    <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Date</div>
                    <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${this.formatDate(ticket.date)}</div>
                  </div>
                  <div class="detail-item" style="text-align: center;">
                    <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Departure</div>
                    <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.departureTime}</div>
                  </div>
                  <div class="detail-item" style="text-align: center;">
                    <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Arrival</div>
                    <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.arrivalTime}</div>
                  </div>
                </div>
              </div>
              
              <div class="passenger-info" style="display: flex; flex-wrap: wrap; justify-content: space-between; margin-bottom: 30px; padding: 15px; background-color: #f0f0f0; border-radius: 8px;">
                <div class="detail-item" style="width: 30%; margin-bottom: 10px; text-align: center;">
                  <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Passenger</div>
                  <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.passengerName}</div>
                </div>
                <div class="detail-item" style="width: 30%; margin-bottom: 10px; text-align: center;">
                  <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Passenger ID</div>
                  <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.passengerId}</div>
                </div>
                <div class="detail-item" style="width: 30%; margin-bottom: 10px; text-align: center;">
                  <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Seat</div>
                  <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.seats && ticket.seats.length > 0 ? ticket.seats[0].id : 'N/A'}</div>
                </div>
                <div class="detail-item" style="width: 30%; margin-bottom: 10px; text-align: center;">
                  <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Class</div>
                  <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${this.getSeatClassName(ticket.seats && ticket.seats.length > 0 ? ticket.seats[0].class : '')}</div>
                </div>
                <div class="detail-item" style="width: 30%; margin-bottom: 10px; text-align: center;">
                  <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Gate</div>
                  <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.gate}</div>
                </div>
                <div class="detail-item" style="width: 30%; margin-bottom: 10px; text-align: center;">
                  <div class="label" style="font-size: 12px; color: #666; margin-bottom: 5px;">Boarding</div>
                  <div class="value" style="font-size: 16px; font-weight: bold; color: #1a1a2e;">${ticket.boardingTime}</div>
                </div>
              </div>
              
              <div class="barcode-section" style="display: flex; flex-direction: column; align-items: center; margin-top: 20px;">
                <svg id="barcode" class="barcode" style="margin-bottom: 10px; height: 50px;"></svg>
                <div class="booking-reference" style="font-size: 14px; font-weight: bold;">
                  Booking Ref: ${ticket.bookingReference}
                </div>
              </div>
            </div>
            
            <div class="ticket-footer" style="background-color: #f0f0f0; padding: 15px; text-align: center; font-size: 14px; color: #666; border-top: 1px dashed #ddd;">
              <p>Thank you for choosing DjangoAIR. We wish you a pleasant flight!</p>
              <p class="small" style="font-size: 12px; margin-top: 5px;">This is an electronic ticket. Please present this document along with a photo ID at the check-in counter.</p>
            </div>
          </div>
        </div>
      `;

      // Генеруємо штрих-код
      const barcodeElement = container.querySelector('#barcode');
      if (barcodeElement && ticket.bookingReference) {
        JsBarcode(barcodeElement, ticket.bookingReference, {
          format: "CODE128",
          lineColor: "#6c63ff",
          width: 2,
          height: 50,
          displayValue: false
        });
      }

      // Чекаємо, щоб DOM повністю оновився
      await new Promise(resolve => setTimeout(resolve, 100));

      // Отримуємо елемент шаблону квитка
      const element = container.querySelector('#ticket-template');

      // Налаштування для PDF
      const options = {
        margin: 0,
        filename: `ticket-${ticket.flightNumber}-${ticket.bookingReference}.pdf`,
        image: { type: 'jpeg', quality: 1 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: {
            unit: 'mm',
            format: [211, 189],    // ширина 200 мм, висота 100 мм
            orientation: 'landscape'  // альбомна орієнтація
          }
      };

      // Генеруємо PDF
      await html2pdf().set(options).from(element).save();

      // Видаляємо тимчасовий контейнер
      document.body.removeChild(container);

      return true;
    } catch (error) {
      console.error('Error generating PDF:', error);
      return false;
    }
  },

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
  }
};

