import { API_SERVER } from './constant.js';
import Dropdown from 'react-bootstrap/Dropdown';
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
      Legend,
      LineElement,
      LinearScale,
      PointElement,
      Title,
      Tooltip,
    );
    this.state = {
      data_keys: null,
      graph_x: null,
      graph_y: null,
      graph_data: null,
    };
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

    let dropdown;
    if (this.state.data_values === null) {
      dropdown = 'Button';
    } else {
      dropdown = 'test';
      //<Dropdown>
      //             <Dropdown.Toggle> DropDown </Dropdown.Toggle>
      //             <Dropdown.Menu>
      //               { this.state.data_values.map( (data) => { return <Dropdown.Item> data[0] </Dropdown.Item/> } ) }
      //             </Dropdown.Menu>
      //           </Dropdown>
    }

    return (
      <div>
        <Line
          data={graphData}
          options={options}
        />
        <button
            onClick={() => {
              fetch(API_SERVER + 'data/list', {method: 'GET'})
                   .then(response => response.json())
                   .then(data => {
                      const json_data = JSON.parse(data);
                      this.setState({
                          data_keys: json_data.columns,
                          data_values: json_data.data,
                      });
                   });
            }}
        >
        { dropdown }
        </button>
      </div>
    );
  }
}

