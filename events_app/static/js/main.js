axios.get('/events')
  .then(response => {
    console.log(response.data)
    const eventTitleLink = document.getElementById('event-title-link')
    let index = 0
    for (event in response.data[index]) {
      let eventHeading = eventTitleLink.appendChild(document.createElement('h4'))
      eventHeading.innerHTML = event.name
      index += 1
    }
  })
  .catch(error => {
    console.log(error)
  })
