import { PieChart } from 'react-minimal-pie-chart';

export default function ConfidencePieChart({row}) {
    return (<PieChart
    label={({ dataEntry }) => String(row.confidence * 100).substring(0, Math.min(String(row.confidence).length, 5)) + "%"}
    labelStyle={(index) => ({
      fill: "#000000",
      fontSize: '13px',
      fontFamily: 'sans-serif',
    })}
    totalValue={1}
    background="#efefef"
      data={[
        { title: 'One', value: row.confidence, color: row.confidence > 0.70 ? '#7eeb3f' : row.confidence > 0.40 ? '#ebb53f': '#e85b56' },
      ]}
    />)
}