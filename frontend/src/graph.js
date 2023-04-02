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
      data_keys: [],
      data_values: null,
      data_table: 'Table',
      data_x: 'Horizontal Axis',
      data_y: 'Vertical Axis',
      graph_x: [],
      graph_y: [],
      data: null,
    };
    this.fetchGraphKeys = this.fetchGraphKeys.bind(this);
    this.fetchGraphValues = this.fetchGraphValues.bind(this);
  }

  componentDidMount() {
    this.fetchGraphKeys();
  }

  fetchGraphValues(table) {
    fetch(API_SERVER + 'data/' + table + '/values', {method: 'GET'})
         .then(response => response.json())
         .then(data => {
            const json_data = JSON.parse(data);
            console.log(json_data.data);
            this.setState({
                data_table: table,
                data_values: json_data.data,
            });
         });
  }

  fetchGraphKeys() {
    fetch(API_SERVER + 'data/keys', {method: 'GET'})
         .then(response => response.json())
         .then(data => {
            const json_data = JSON.parse(data);
            this.setState({
                data_keys: json_data.data,
            });
         });
  }

  render() {
    const graphData = {
      labels: this.state.graph_x,
      datasets: [
        {
          label: "test1",
          data: this.state.graph_y,
          borderColor: "rgb(75,192,129)",
        }
      ]
    };

    const options: {} = {
      maintainAspectRation: false,
    };

    return <>
      <Line
        data={graphData}
        options={options}
      />

      <table frame='border' cellPadding='5%'>
        <thead>
          <tr>
            <th>
              Key
            </th>
            <th>
              Value
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td align='right'>
              Table
            </td>
            <td>
              <Dropdown>
                <Dropdown.Toggle>
                  { this.state.data_table }
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  {
                    this.state.data_keys.map( 
                      (data) => {
                        return (
                          <Dropdown.Item
                              key={'table_' + data[0]}
                              onClick={()=>this.fetchGraphValues(data[0])}
                          >
                            { data[0] }
                          </Dropdown.Item>
                        )
                      }
                    )
                  }
                </Dropdown.Menu>
              </Dropdown>
            </td>
          </tr>
          <tr>
            <td align='right'>
              Horizontal Axis
            </td>
            <td>
              <Dropdown>
                <Dropdown.Toggle>
                  { this.state.data_x }
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  {
                    this.state.data_keys.filter((data)=>{ return this.state.data_table === data[0] }).map( 
                      (data) => {
                        return data.filter((value)=>{ return value !== null && value !== this.state.data_table }).map((value) => {
                          return (
                            <Dropdown.Item
                                key={'x_' + value}
                                onClick={() => {
                                    const graph_x_index = data.indexOf(value);
                                    this.setState({
                                        graph_x: this.state.data_values.map((data_value) => data_value[graph_x_index]),
                                        data_x: value
                                    })
                                }}
                            >
                              { value }
                            </Dropdown.Item>
                          )
                        })
                      }
                    )
                  }
                </Dropdown.Menu>
              </Dropdown>
            </td>
          </tr>
          <tr>
            <td align='right'>
              Vertical Axis
            </td>
            <td>
              <Dropdown>
                <Dropdown.Toggle>
                  { this.state.data_y }
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  {
                    this.state.data_keys.filter((data)=>{ return this.state.data_table === data[0] }).map( 
                      (data) => {
                        return data.filter((value)=>{ return value !== null && value !== this.state.data_table }).map((value) => {
                          return (
                            <Dropdown.Item
                                key={'y_' + value}
                                onClick={() => {
                                    const graph_y_index = data.indexOf(value);
                                    this.setState({
                                        graph_y: this.state.data_values.map((data_value) => data_value[graph_y_index]),
                                        data_y: value
                                    })
                                }}
                            >
                              { value }
                            </Dropdown.Item>
                          )
                        })
                      }
                    )
                  }
                </Dropdown.Menu>
              </Dropdown>
            </td>
          </tr>
        </tbody>
      </table>


    </>
  }
}

