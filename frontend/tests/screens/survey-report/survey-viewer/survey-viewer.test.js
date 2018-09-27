import React from 'react';
import SurveyViewer from '../../../../src/screens/survey-report/survey-viewer/survey-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('SurveyViewer', () => {
  let surveyViewer;
  beforeEach(() => {
    surveyViewer = (
      <SurveyViewer
        startDate={'20191017T00:00:00'}
        endDate={'20191017T00:00:00'}
      />
    );
  });

  it('mounts', () => {
    mount(surveyViewer);
  });
});
