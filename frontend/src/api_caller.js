import React from 'react';
import axios from 'axios';
import { API } from './constant.js'

export default class ApiCaller extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      message: "test",
    };
  }

  render() {
    return(
      <div>
        <button
          className="TestApi"
          onClick={() => axios.get(API.TEST)
            .then(response => {
              const received_message = response.data.message
              this.setState({message: received_message});
            })
          }
        >
          { this.state.message }
        </button>
      </div>

    );
  }
}
