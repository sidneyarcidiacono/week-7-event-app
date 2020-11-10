const startAddEvent = document.getElementById('start-add-event')
const startEditEvent = document.getElementById('start-edit-event')
const editEventForm = document.getElementById('edit-event-form')
const addEventForm = document.getElementById('add-event-form')

const addEventHandler = () => {
  addEventForm.style.display = 'flex'
}

const editEventHandler = () => {
  editEventForm.style.display = 'flex'
}

startAddEvent.addEventListener('click', addEventHandler)
startEditEvent.addEventListener ('click', editEventHandler)
