class EventDisplay {
  constructor (event) {
    this.eventHeading = document.createElement('h4');
    this.name = event.title;
    this.date = document.createElement('p');
    this.time = document.createElement('p');
    this.description = document.createElement('p');
  }

  set () {
    this.eventHeading.innerHTML = this.name
  }
}

axios.get('/events')
  .then(response => {
    const eventTitleLink = document.getElementById('event-title-link')
    let index = 0
    for (event of response.data.data) {
      console.log(event)
      display = new EventDisplay(event)
      display.set()
      console.log(display)
      index += 1
    }
  })
  .catch(error => {
    console.log(error)
  })
