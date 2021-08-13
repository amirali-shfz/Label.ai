import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const tableTextStyle = {
  //fontSize:"40px" // TODO: make text look nice
};

export default function NewConfidenceTable({ rows }) {
  const classes = useStyles();

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Image</TableCell>
            <TableCell align="middle">Label</TableCell>
            <TableCell align="middle">Total Votes</TableCell>
            <TableCell align="middle">Confidence</TableCell>
            <TableCell align="middle">Url</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.img_id}>
              <TableCell component="th" scope="row">
                <img
                  onError={(e) => e.target.removeAttribute("src")}
                  style={{ maxHeight: "400px", maxWidth: "400px" }}
                  src={row.url}
                  alt={`example of ${row.label_id}`}
                />
              </TableCell>
              <TableCell
                style={Object.assign(tableTextStyle, {})}
                align="middle"
              >
                {row.label}
              </TableCell>
              <TableCell
                style={Object.assign(tableTextStyle, {})}
                align="middle"
              >
                {Math.round(row.total_votes)}
              </TableCell>
              <TableCell
                style={Object.assign(tableTextStyle, {})}
                align="middle"
              >
                {String(row.confidence).substring(
                  0,
                  Math.min(String(row.confidence).length, 6)
                )}
              </TableCell>
              <TableCell
                style={Object.assign(tableTextStyle, {})}
                align="middle"
              >
                <a href={row.url} rel="noreferrer">
                  {" "}
                  link
                </a>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
