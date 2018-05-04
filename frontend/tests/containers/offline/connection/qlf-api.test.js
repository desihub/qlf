import QlfApi from '../../../../src/containers/offline/connection/qlf-api';

describe('QlfApi', () => {
  beforeEach(() => {
    fetch.mockReset();
  });

  it('calls getQA', () => {
    QlfApi.getQA(1);
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/single_qa/1/?format=json',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  // it('calls getProcessingHistory', () => {
  //   QlfApi.getProcessingHistory();
  //   expect(fetch).toBeCalledWith(
  //     'http://localhost:8001/dashboard/api/processing_history/?format=json',
  //     {
  //       headers: {
  //         _headers: {
  //           accept: ['application/json'],
  //           'content-type': ['application/json'],
  //         },
  //       },
  //       method: 'GET',
  //     }
  //   );
  // });

  it('calls sendTicketMail', () => {
    QlfApi.sendTicketMail('hawk@tes.com', 'test', 'problem', 'hawk');
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/send_ticket_email/?format=json&email=hawk@tes.com&message=test&subject=problem&name=hawk',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });
});
