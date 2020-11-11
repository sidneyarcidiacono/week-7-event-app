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
