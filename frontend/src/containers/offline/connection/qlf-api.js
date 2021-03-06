const apiUrl =
  process.env.NODE_ENV !== 'development'
    ? window.origin + '/'
    : process.env.REACT_APP_API;
const headers = new Headers({
  Accept: 'application/json',
  'Content-Type': 'application/json',
});

export default class QlfApi {
  static async getQA(processId) {
    try {
      const qa = await fetch(
        `${apiUrl}dashboard/api/processing_history/${processId}/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await qa.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getLastProcess() {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/last_process/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async reprocessExposure(exposure) {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/add_exposure/?format=json&exposure_id=${
          exposure
        }`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getProcessingHistoryById(processId) {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/${processId}/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getCurrentConfiguration() {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/current_configuration/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getCurrentThresholds() {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/disk_thresholds/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getDefaultConfiguration() {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/default_configuration/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getQlConfig(config) {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/qlconfig/?format=json&type=${config}`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getExposuresDateRange() {
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/exposures_date_range/`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await exposures.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getFlavors() {
    try {
      const flavors = await fetch(`${apiUrl}dashboard/api/distinct_flavors/`, {
        method: 'GET',
        headers: headers,
      });
      const responseJson = await flavors.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getNights() {
    try {
      const nights = await fetch(`${apiUrl}dashboard/api/distinct_nights/`, {
        method: 'GET',
        headers: headers,
      });
      const responseJson = await nights.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getProcessingHistory(start, end, order, offset, limit, filters) {
    if (!start && !end) return;
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/?format=json&limit=${
          limit
        }&offset=${offset}&ordering=${order}&datemin=${
          start.split('T')[0]
        }&datemax=${end.split('T')[0]}&${filters}`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getObservingHistory(start, end, order, offset, limit, filters) {
    if (!start && !end) return;
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/observing_history/?format=json&limit=${
          limit
        }&offset=${offset}&ordering=${order}&datemin=${
          start.split('T')[0]
        }&datemax=${end.split('T')[0]}&${filters}`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await exposures.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getSurveyReport(night, order, filters) {
    if (!night) return;
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/observing_history/?format=json&night=${
          night
        }&ordering=${order}&${filters}`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await exposures.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async addProcessComment(text, process) {
    const body = {
      text,
      process,
      user: 1,
    };
    const commentResponse = await fetch(
      `${apiUrl}dashboard/api/process_comment/`,
      {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
      }
    );
    const responseJson = await commentResponse.json();
    return responseJson;
  }

  static async deleteProcessComment(commentId) {
    await fetch(`${apiUrl}dashboard/api/process_comment/${commentId}/`, {
      method: 'DELETE',
      headers: headers,
    });
  }

  static async updateProcessComment(commentId, process, text) {
    const body = {
      text,
      process,
    };
    const commentResponse = await fetch(
      `${apiUrl}dashboard/api/process_comment/${commentId}/`,
      {
        method: 'PUT',
        headers: headers,
        body: JSON.stringify(body),
      }
    );
    return commentResponse.json();
  }

  static async getProcessComments(processId) {
    const commentResponse = await fetch(
      `${apiUrl}dashboard/api/process_comment/?process=${processId}`,
      {
        method: 'GET',
        headers: headers,
      }
    );
    return commentResponse.json();
  }

  static async getCameraLog(processId, arm, spectrograph) {
    const cameraLog = await fetch(
      `${apiUrl}dashboard/get_camera_log/?process=${processId}&camera=${arm}${
        spectrograph
      }`,
      {
        method: 'GET',
        headers: headers,
      }
    );
    return cameraLog.json();
  }

  static async sendTicketMail(email, message, subject, name) {
    const ticket = await fetch(
      `${apiUrl}send_ticket_email/?format=json&email=${email}&message=${
        message
      }&subject=${subject}&name=${name}`,
      {
        method: 'GET',
        headers: headers,
      }
    );
    const responseJson = await ticket.json();
    return responseJson;
  }

  static async getObjectData(startDate, endDate, program) {
    const objectData = await fetch(
      `${apiUrl}dashboard/footprint_object_type_count?start=${startDate}&end=${
        endDate
      }&program=${program}`,
      {
        method: 'GET',
        headers: headers,
      }
    );
    const responseJson = await objectData.json();
    return responseJson;
  }

  static async checkViewFiles(processId) {
    try {
      const check = await fetch(
        `${apiUrl}dashboard/api/check_view_files/?format=json&process_id=${
          processId
        }`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await check.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }
}
