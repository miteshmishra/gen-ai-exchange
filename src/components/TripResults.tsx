import { Paper, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

interface TripResultsProps {
  results?: {
    destination: string;
    activities: string[];
    recommendations: string[];
  };
}

const TripResults = ({ results }: TripResultsProps) => {
  if (!results) {
    return null;
  }

  return (
    <Paper elevation={3} sx={{ p: { xs: 2, sm: 3 }, mt: 3 }}>
      <Typography variant="h2" gutterBottom sx={{ fontSize: { xs: '1.5rem', sm: '2rem' } }}>
        Your Trip Plan for {results.destination}
      </Typography>
      
      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Recommended Activities
      </Typography>
      <List>
        {results.activities.map((activity, index) => (
          <ListItem key={index}>
            <ListItemText primary={activity} />
          </ListItem>
        ))}
      </List>

      <Divider sx={{ my: 2 }} />

      <Typography variant="h6" gutterBottom>
        Travel Tips & Recommendations
      </Typography>
      <List>
        {results.recommendations.map((recommendation, index) => (
          <ListItem key={index}>
            <ListItemText primary={recommendation} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default TripResults;