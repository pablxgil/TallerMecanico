import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'tallerTheme',
    themes: {
      tallerTheme: { dark: false, colors: { primary: '#174A5E', secondary: '#E6A23C', accent: '#3E8E7E', error: '#BA1A1A', background: '#F6F8F8', surface: '#FFFFFF' } }
    }
  }
})

