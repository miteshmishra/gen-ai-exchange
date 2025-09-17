import { Paper, TextField, Button, Typography } from '@mui/material';
import { Grid } from '@mui/material';
import { useState } from 'react';
import type { ChangeEvent, FormEvent } from 'react';

interface TripFormData {
  destination: string;
  startDate: string;
  duration: string;
  preferences: string;
}

const TripForm = () => {
  const [formData, setFormData] = useState({
    destination: '',
    startDate: '',
    duration: '',
    preferences: ''
  });

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // TODO: Handle form submission
    console.log(formData);
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Paper elevation={3} sx={{ p: { xs: 2, sm: 3 }, mb: 3 }}>
      <Typography variant="h2" gutterBottom sx={{ fontSize: { xs: '1.5rem', sm: '2rem' } }}>
        Plan Your Trip
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Where do you want to go?"
              name="destination"
              value={formData.destination}
              onChange={handleChange}
              required
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="date"
              label="Start Date"
              name="startDate"
              value={formData.startDate}
              onChange={handleChange}
              required
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Duration (days)"
              name="duration"
              type="number"
              value={formData.duration}
              onChange={handleChange}
              required
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Travel Preferences"
              name="preferences"
              multiline
              rows={4}
              value={formData.preferences}
              onChange={handleChange}
              placeholder="Tell us about your interests (e.g., adventure, culture, relaxation)"
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              fullWidth
              sx={{ mt: 2 }}
            >
              Generate Trip Plan
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default TripForm;