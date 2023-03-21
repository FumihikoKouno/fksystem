import axios from 'axios';
import { API_SERVER } from './constant.js';
import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";


export default class LegendGraph extends React.Component {
  constructor(props) {
    super(props);
    ChartJS.register(
      CategoryScale,
      LinearScale,
      PointElement,
      LineElement,
      Title,
      Tooltip,
      Legend
    );
    this.state = { data_list: null };
  }

  render() {
    const graphData = {
      labels: [1, 2, 3, 4, 5, 6],
      datasets: [
        {
          label: "test1",
          data: [1, 31, 32, 12, 33, 2],
          borderColor: "rgb(75,192,129)",
        }
      ]
    };

    const options: {} = {
      maintainAspectRation: false,
    };

    return (
      <div>
        <Line
          data={graphData}
          options={options}
        />
        <button
            onClick={() => {
              axios.get(API_SERVER + 'data/list')
                   .then(response => {
                      console.log(response.data);
                      this.setState({ data_list: response.data })
                   });
            }}
        >
            { this.state.data_list }
        </button>
      </div>
    );
  }
}

