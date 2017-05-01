# Copyright 2016 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. All Rights Reserved.
#
# Portion of this code is Copyright Geoscience Australia, Licensed under the
# Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License
# at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# The CEOS 2 platform is licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django import forms

import datetime

from .models import ResultType
from apps.dc_algorithm.models import Area, Compositor, AnimationType
"""
File designed to house the different forms for taking in user input in the web application.  Forms
allow for input validation and passing of data.  Includes forms for creating Queries to be ran.
"""

# Author: AHDS
# Creation date: 2016-06-23
# Modified by:
# Last modified date:


class DataSelectForm(forms.Form):
    """
    Django form to be created for selecting information and validating input for:
        result_type
        band_selection
        title
        description
    Init function to initialize dynamic forms.
    """

    #these are done in the init funct.
    query_type = forms.ModelChoiceField(
        queryset=None,
        to_field_name="result_id",
        empty_label=None,
        help_text='Select the type of image you would like displayed.',
        label='Result Type (Map view/png):',
        widget=forms.Select(attrs={'class': 'field-long tooltipped'}))

    compositor = forms.ModelChoiceField(
        queryset=None,
        to_field_name="id",
        empty_label=None,
        help_text='Select the method by which the "best" pixel will be chosen.',
        label="Compositing Method:",
        widget=forms.Select(attrs={'class': 'field-long tooltipped'}))

    animated_product = forms.ModelChoiceField(
        queryset=None,
        to_field_name="id",
        empty_label=None,
        help_text='Generate a .gif containing either scene data or the cumulative mosaic over time. This is not compatible with median pixel mosaics.',
        label='Generate Time Series Animation',
        widget=forms.Select(attrs={'class': 'field-long tooltipped'}))

    def __init__(self, *args, **kwargs):
        datacube_platform = kwargs.pop('datacube_platform', None)
        super(DataSelectForm, self).__init__(*args, **kwargs)
        self.fields["query_type"].queryset = ResultType.objects.filter(datacube_platform=datacube_platform
                                                                       if datacube_platform is not None else
                                                                       args[0].get('platform'))
        self.fields["compositor"].queryset = Compositor.objects.all()
        self.fields["animated_product"].queryset = AnimationType.objects.filter(
            app_name__in=["custom_mosaic_tool", "all"]).order_by('app_name', 'id')
