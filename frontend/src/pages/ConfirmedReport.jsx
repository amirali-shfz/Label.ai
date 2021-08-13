import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import ConfidenceTable from "./Table";
const ConfirmedPage = ({ label, setLabel, allLabels, data, reportName }) => {
  return (
    <>
      <FormControl>
        <InputLabel id="select-label">Label</InputLabel>
        <Select
          labelId="simple-select-label"
          id="simple-select"
          value={label}
          onChange={(event) => {
            setLabel(event.target.value);
          }}
        >
          {allLabels === undefined
            ? null
            : allLabels.map((label) => {
                return <MenuItem value={label.label_id}>{label.name}</MenuItem>;
              })}
        </Select>
      </FormControl>
      <ConfidenceTable rows={data === undefined ? [] : data}></ConfidenceTable>
    </>
  );
  //Todo make this work
  //  const [inputValue, setInputValue] = React.useState('');
  /* <Autocomplete
          value={label}
          onChange={(event, newValue) => {
            setLabel(newValue)
          }}
          inputValue={inputValue}
          onInputChange={(event, newInputValue) => {
            setInputValue(newInputValue);
          }}
          options={allLabels === undefined ? [] : allLabels}
          getOptionLabel={(option) => option.name}
          style={{ width: 400, marginBottom: 40 }}
          renderInput={(params) => <TextField {...params} label="Labels" variant="outlined" />}
        /> */
};

export default ConfirmedPage;
