import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { PieChart } from 'react-minimal-pie-chart';
import ConfidencePieChart from './ConfidencePieChart';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const tableTextStyle = {
  fontSize:"17px"
};

export default function ConfidenceTable({ rows }) {
  const classes = useStyles();

  return (
    
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell style={Object.assign(tableTextStyle, {})} align="center">Image</TableCell>
            <TableCell style={Object.assign(tableTextStyle, {})} align="center">Total Votes</TableCell>
            <TableCell style={Object.assign(tableTextStyle, {})} align="center">Confidence</TableCell>
            <TableCell style={Object.assign(tableTextStyle, {})} align="center">URL</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.img_id}>
              <TableCell align="center" component="th" scope="row">
                <img 
                onError={(e) => e.target.removeAttribute('src')} 
                style={{maxHeight:"375px", maxWidth:"375px"}} 
                src={row.url} alt={`example of ${row.label_id}`}/>
              </TableCell>
              <TableCell style={Object.assign(tableTextStyle, {})} align="center">{Math.round(row.total_votes)}</TableCell>
              <TableCell style={Object.assign(tableTextStyle, {})} align="center">

                <ConfidencePieChart row={row}></ConfidencePieChart>
                </TableCell>
              <TableCell style={Object.assign(tableTextStyle, {})} align="center">
                <Button href={row.url} color="primary">
                  Link
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
