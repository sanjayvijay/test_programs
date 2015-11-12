import ctypes as C

class Edge:
    def __init__(self, verbose=True):
        self.camera_handle = C.c_void_p(0)
        if verbose: print("Opening pco.edge camera...")
        try:
            assert self.camera_handle.value is None
            dll.open_camera(self.camera_handle, 0)
            assert self.camera_handle.value is not None
        except (WindowsError, AssertionError):
            print("Failed to open pco.edge camera.")
            print(" *Is the camera on, and plugged into the computer?")
            print(" *Is CamWare running?")
            print(" *Is sc2_cl_me4.dll in the same directory as SC2_Cam.dll?")
            raise
        self.verbose = verbose
        self.buffer_numbers = []
        if self.verbose: print(" Camera open.")
        self.disarm()
        self._refresh_camera_setting_attributes()
        return None                            

    def close(self):
        if self.verbose: print("Closing pco.edge camera...")
        dll.close_camera(self.camera_handle)
        if self.verbose: print(" Camera closed.")

    def apply_settings(
        self,
        trigger='auto_trigger',
        exposure_time_microseconds=2200,
        region_of_interest=(1, 1, 2060, 2048)):
        """
        'trigger' can be:
         'auto_trigger' or 'external_trigger'
        See the comment block in _get_trigger_mode() for further details.

        'exposure_time_microseconds' can be as low as 107 and as high
        as 1000000
        """    
        self.disarm()
        if self.verbose: print("Applying settings to camera...")
        dll.reset_settings_to_default(self.camera_handle)        
        self._set_sensor_format('standard')
        self._set_trigger_mode(trigger)
        self._set_storage_mode('recorder')
        self._set_recorder_submode('ring_buffer')
        self._set_acquire_mode('auto')

        
        """
        It's good to check the camera health periodically. Now's as good
        a time as any, especially since the expected result is
        predictable: it should all be zeros.
        """
        camera_health = self._get_camera_health()
        for v in camera_health.values():
            assert v == 0

        
        return None
        
        
        
##        wSensor = ctypes.c_uint16(0)
##        if verbose:
##            print "Setting sensor format..."
##        PCO_api.PCO_SetSensorFormat(self.camera_handle, wSensor)
##        PCO_api.PCO_GetSensorFormat(self.camera_handle, ctypes.byref(wSensor))
##        mode_names = {0: "standard", 1:"extended"}
##        if verbose:
##            print " Sensor format is", mode_names[wSensor.value]
##
##        if verbose:
##            print "Getting camera health status..."
##        dwWarn, dwErr, dwStatus = (
##            ctypes.c_uint32(), ctypes.c_uint32(), ctypes.c_uint32())
##        response = PCO_api.PCO_GetCameraHealthStatus(
##            self.camera_handle,
##            ctypes.byref(dwWarn), ctypes.byref(dwErr), ctypes.byref(dwStatus))
##        if verbose:
##            print " Camera health status (0 0 0 means healthy):",
##            print dwWarn.value, dwErr.value, dwStatus.value
##        if dwWarn.value != 0 or dwErr.value != 0 or dwStatus.value != 0:
##            raise UserWarning("Camera unhealthy: %x %x %x %i"%(
##                dwWarn.value, dwErr.value, dwStatus.value, response))
##
##        if verbose:
##            print "Reading temperatures..."
##        ccdtemp, camtemp, powtemp = (
##            ctypes.c_int16(), ctypes.c_int16(), ctypes.c_int16())
##        PCO_api.PCO_GetTemperature(
##            self.camera_handle,
##            ctypes.byref(ccdtemp), ctypes.byref(camtemp), ctypes.byref(powtemp))
##        if verbose:
##            print " CCD temperature:", ccdtemp.value * 0.1, "C"
##            print " Camera temperature:", camtemp.value, "C"
##            print " Power supply temperature:", powtemp.value, "C"
##
##        """
##        0x0000 = [auto trigger]
##        A new image exposure is automatically started best possible
##        compared to the readout of an image. If a CCD is used and the
##        images are taken in a sequence, then exposures and sensor readout
##        are started simultaneously. Signals at the trigger input (<exp
##        trig>) are irrelevant.
##        - 0x0001 = [software trigger]:
##        An exposure can only be started by a force trigger command.
##        - 0x0002 = [extern exposure & software trigger]:
##        A delay / exposure sequence is started at the RISING or FALLING
##        edge (depending on the DIP switch setting) of the trigger input
##        (<exp trig>).
##        - 0x0003 = [extern exposure control]:
##        The exposure time is defined by the pulse length at the trigger
##        input(<exp trig>). The delay and exposure time values defined by
##        the set/request delay and exposure command are ineffective.
##        (Exposure time length control is also possible for double image
##        mode; exposure time of the second image is given by the readout
##        time of the first image.)
##        """
##        trigger_mode_names = {0: "auto trigger",
##                      1: "software trigger",
##                      2: "external trigger/software exposure control",
##                      3: "external exposure control"}
##        mode_name_to_number = dict(
##            (v,k) for k, v in trigger_mode_names.iteritems())
##        if verbose:
##            print "Setting trigger mode..."
##        wTriggerMode = ctypes.c_uint16(mode_name_to_number[trigger])
##        PCO_api.PCO_SetTriggerMode(self.camera_handle, wTriggerMode)
##        PCO_api.PCO_GetTriggerMode(
##            self.camera_handle, ctypes.byref(wTriggerMode))
##        if verbose:
##            print " Trigger mode is", trigger_mode_names[wTriggerMode.value]
##
##        wStorageMode = ctypes.c_uint16()
##        PCO_api.PCO_GetStorageMode(
##            self.camera_handle, ctypes.byref(wStorageMode))
##        mode_names = {0: "Recorder", 1: "FIFO buffer"}#Not critical for pco.edge
##        if verbose:
##            print "Storage mode:", mode_names[wStorageMode.value]
##
##        if verbose:
##            print "Setting recorder submode..."
##        wRecSubmode = ctypes.c_uint16(1)
##        PCO_api.PCO_SetRecorderSubmode(self.camera_handle, wRecSubmode)
##        PCO_api.PCO_GetRecorderSubmode(
##            self.camera_handle, ctypes.byref(wRecSubmode))
##        mode_names = {0: "sequence", 1: "ring buffer"}
##        if verbose:
##            print " Recorder submode:", mode_names[wRecSubmode.value]
##
##        if verbose:
##            print "Setting acquire mode..."
##        wAcquMode = ctypes.c_uint16(0)
##        PCO_api.PCO_SetAcquireMode(self.camera_handle, wAcquMode)
##        PCO_api.PCO_GetAcquireMode(self.camera_handle, ctypes.byref(wAcquMode))
##        mode_names = {0: "auto", 1:"external (static)", 2:"external (dynamic)"}
##        if verbose:
##            print " Acquire mode:", mode_names[wAcquMode.value]
##
##        if verbose:
##            print "Setting pixel rate..."
##        if self.pco_edge_type == '4.2':
##            dwPixelRate = ctypes.c_uint32(272250000)
##        elif self.pco_edge_type == '5.5':
##            dwPixelRate = ctypes.c_uint32(286000000)
##        else:
##            raise UserWarning("Unknown PCO edge type")
##        PCO_api.PCO_SetPixelRate(self.camera_handle, dwPixelRate)
##        PCO_api.PCO_GetPixelRate(self.camera_handle, ctypes.byref(dwPixelRate))
##        if verbose:
##            print " Pixel rate:", dwPixelRate.value
##
##        if verbose:
##            print "Setting delay and exposure time..."
##        if 500 > exposure_time_microseconds < 1000000:
##            raise UserWarning(
##                "exposure_time_microseconds must be between 500 and 1000000")
##        dwDelay = ctypes.c_uint32(0)
##        wTimeBaseDelay = ctypes.c_uint16(0)
##        dwExposure = ctypes.c_uint32(int(exposure_time_microseconds))
##        wTimeBaseExposure = ctypes.c_uint16(1)
##        PCO_api.PCO_SetDelayExposureTime(
##            self.camera_handle,
##            dwDelay, dwExposure, wTimeBaseDelay, wTimeBaseExposure)
##        PCO_api.PCO_GetDelayExposureTime(
##            self.camera_handle,
##            ctypes.byref(dwDelay), ctypes.byref(dwExposure),
##            ctypes.byref(wTimeBaseDelay), ctypes.byref(wTimeBaseExposure))
##        mode_names = {0: "nanoseconds", 1: "microseconds", 2: "milliseconds"}
##        if verbose:
##            print " Exposure:", dwExposure.value, mode_names[wTimeBaseExposure.value]
##            print " Delay:", dwDelay.value, mode_names[wTimeBaseDelay.value]
##
##        x0, y0, x1, y1 = enforce_roi(
##            region_of_interest,
##            pco_edge_type=self.pco_edge_type,
##            verbose=verbose)
##
##        wRoiX0, wRoiY0, wRoiX1, wRoiY1 = (
##            ctypes.c_uint16(x0), ctypes.c_uint16(y0),
##            ctypes.c_uint16(x1), ctypes.c_uint16(y1))
##        if verbose:
##            print "Setting sensor ROI..."
##        PCO_api.PCO_SetROI(self.camera_handle, wRoiX0, wRoiY0, wRoiX1, wRoiY1)
##        PCO_api.PCO_GetROI(self.camera_handle,
##                           ctypes.byref(wRoiX0), ctypes.byref(wRoiY0),
##                           ctypes.byref(wRoiX1), ctypes.byref(wRoiY1))
##        if verbose:
##            print " Camera ROI:"
##            """We typically use 841 to 1320 u/d, 961 to 1440 l/r  for the 5.5"""
##            print "  From pixel", wRoiX0.value,
##            print "to pixel", wRoiX1.value, "(left/right)"
##            print "  From pixel", wRoiY0.value,
##            print "to pixel", wRoiY1.value, "(up/down)"
##            print
##
##        if hasattr(self, '_prepared_to_record'):
##            del self._prepared_to_record
##
##        trigger = trigger_mode_names[wTriggerMode.value]
##        """Exposure is in microseconds"""
##        exposure = dwExposure.value * 10.**(3*wTimeBaseExposure.value - 3)
##        roi = (wRoiX0.value, wRoiY0.value,
##               wRoiX1.value, wRoiY1.value)
##        return (trigger, exposure, roi)

    def arm(self):
        pass

##        def arm(self, num_buffers=2, verbose=False):
##        if self.armed:
##            raise UserWarning('The pco.edge camera is already armed.')
##        if verbose:
##            print "Arming camera..." 
##        PCO_api.PCO_ArmCamera(self.camera_handle)
##        self.wXRes, self.wYRes, wXResMax, wYResMax = (
##            ctypes.c_uint16(), ctypes.c_uint16(),
##            ctypes.c_uint16(), ctypes.c_uint16())
##        PCO_api.PCO_GetSizes(self.camera_handle,
##                             ctypes.byref(self.wXRes), ctypes.byref(self.wYRes),
##                             ctypes.byref(wXResMax), ctypes.byref(wYResMax))
##        if verbose:
##            print "Camera ROI dimensions:",
##            print self.wXRes.value, "(l/r) by", self.wYRes.value, "(u/d)"
##
##        dwSize = ctypes.c_uint32(self.wXRes.value * self.wYRes.value * 2)
##        self.buffer_numbers, self.buffer_pointers, self.buffer_events = (
##            [], [], [])
##        for i in range(num_buffers):
##            self.buffer_numbers.append(ctypes.c_int16(-1))
##            self.buffer_pointers.append(ctypes.c_void_p(0))
##            self.buffer_events.append(ctypes.c_void_p(0))
##            PCO_api.PCO_AllocateBuffer(
##                self.camera_handle, ctypes.byref(self.buffer_numbers[i]),
##                dwSize, ctypes.byref(self.buffer_pointers[i]),
##                ctypes.byref(self.buffer_events[i]))
##            if verbose:
##                print "Buffer number", self.buffer_nubmers[i].value,
##                print "is at address", self.buffer_pointers[i],
##                print "linked to an event containing:",
##                print self.buffer_events[i].value
##
##        PCO_api.PCO_CamLinkSetImageParameters(
##            self.camera_handle, self.wXRes, self.wYRes)
##
##        wRecState = ctypes.c_uint16(1)
##        message = PCO_api.PCO_SetRecordingState(self.camera_handle, wRecState)
##        if verbose:
##            print "Recording state return value:", message
##        self.armed = True
##        return None

    def disarm(self):
        if self.verbose: print("Disarming camera...")
        wRecState = C.c_uint16(0) #turn off recording
        dll.set_recording_state(self.camera_handle, wRecState)
        dll.remove_buffer(self.camera_handle)
        for buf in self.buffer_numbers: #free any allocated buffers
            dll.free_buffer(self.camera_handle, buf)
        self.buffer_numbers, self.buffer_pointers, self.buffer_events = (
            [], [], [])
        if hasattr(self, '_prepared_to_record'):
            del self._prepared_to_record
        self.armed = False
        if self.verbose: print(" Camera disarmed.")
        return None

    def record_to_memory(self):
        pass
    
    def _refresh_camera_setting_attributes(self):
        """
        There are two ways to access a camera setting:
        
         1. Ask the camera directly, using a self.get_*() - type method.
        
          This interrogates the camera via a DLL call, updates the
          relevant attribute(s) of the Edge object, and returns the
          relevant value(s). This is slower, because you have to wait for
          round-trip communication, but gets you up-to-date info.

         2. Access an attribute of the Edge object, e.g. self.roi

          This ignores the camera, which is very fast, but the resulting
          value could potentially be inconsistent with the camera's true
          setting (although I hope it isn't!)

        _refresh_camera_setting_attributes() is a convenience function
        to update all the camera attributes at once. Call it if you're
        nervous, I guess.
        """
        if self.verbose: print("Retrieving settings from camera...")
        self._get_sensor_format()
        self._get_camera_health()
        self._get_temperature()
        self._get_trigger_mode()
        self._get_storage_mode()
        self._get_recorder_submode()
        self._get_acquire_mode()
        self._get_pixel_rate()
        self._get_exposure_time()
        self._get_roi()
        return None

    def _get_sensor_format(self):
        wSensor = C.c_uint16(777) #777 is not an expected output
        dll.get_sensor_format(self.camera_handle, wSensor)
        assert wSensor.value in (0, 1) #wSensor.value should change
        mode_names = {0: "standard", 1: "extended"}
        if self.verbose: print(" Sensor format:", mode_names[wSensor.value])
        self.sensor_format = mode_names[wSensor.value]
        return self.sensor_format

    def _set_sensor_format(self, mode='standard'):
        mode_numbers = {"standard": 0, "extended": 1}
        if self.verbose:
            print(" Setting sensor format to:", mode)
        wSensor = C.c_uint16(mode_numbers[mode])
        dll.set_sensor_format(self.camera_handle, wSensor)
        assert self._get_sensor_format() == mode
        return self.sensor_format
    
    def _get_camera_health(self):
        dwWarn, dwErr, dwStatus = (
            C.c_uint32(), C.c_uint32(), C.c_uint32())
        dll.get_camera_health(self.camera_handle, dwWarn, dwErr, dwStatus)
        if self.verbose:
            print(" Camera health status:")
            print("  Warnings:", dwWarn.value, "(0 means healthy)")
            print("  Errors:", dwErr.value, "(0 means healthy)")
            print("  Status:", dwStatus.value)
        self.camera_health = {
            'warnings': dwWarn.value,
            'errors': dwErr.value,
            'status': dwStatus.value}
        return self.camera_health

    def _get_temperature(self):
        ccdtemp, camtemp, powtemp = (
            C.c_int16(), C.c_int16(), C.c_int16())
        dll.get_temperature(self.camera_handle, ccdtemp, camtemp, powtemp)
        if self.verbose:
            print(" CCD temperature:", ccdtemp.value * 0.1, "C")
            print(" Camera temperature:", camtemp.value, "C")
            print(" Power supply temperature:", powtemp.value, "C")
        self.temperature = {
            'ccd_temp': ccdtemp.value * 0.1,
            'camera_temp': camtemp.value,
            'power_supply_temp': powtemp.value}
        return self.temperature

    def _get_trigger_mode(self):
        """
        0x0000 = [auto trigger]
        A new image exposure is automatically started best possible
        compared to the readout of an image. If a CCD is used and the
        images are taken in a sequence, then exposures and sensor readout
        are started simultaneously. Signals at the trigger input (<exp
        trig>) are irrelevant.
        - 0x0001 = [software trigger]:
        An exposure can only be started by a force trigger command.
        - 0x0002 = [extern exposure & software trigger]:
        A delay / exposure sequence is started at the RISING or FALLING
        edge (depending on the DIP switch setting) of the trigger input
        (<exp trig>).
        - 0x0003 = [extern exposure control]:
        The exposure time is defined by the pulse length at the trigger
        input(<exp trig>). The delay and exposure time values defined by
        the set/request delay and exposure command are ineffective.
        (Exposure time length control is also possible for double image
        mode; exposure time of the second image is given by the readout
        time of the first image.)
        """
        trigger_mode_names = {0: "auto_trigger",
                              1: "software_trigger",
                              2: "external_trigger",
                              3: "external_exposure"}
        wTriggerMode = C.c_uint16()
        dll.get_trigger_mode(self.camera_handle, wTriggerMode)
        if self.verbose:
            print(" Trigger mode:", trigger_mode_names[wTriggerMode.value])
        self.trigger_mode = trigger_mode_names[wTriggerMode.value]
        return self.trigger_mode
    
    def _set_trigger_mode(self, mode="auto_trigger"):
        trigger_mode_numbers = {
            "auto_trigger": 0,
            "external_trigger": 2}
        if self.verbose: print(" Setting trigger mode to:", mode)
        wTriggerMode = C.c_uint16(trigger_mode_numbers[mode])
        dll.set_trigger_mode(self.camera_handle, wTriggerMode)
        assert self._get_trigger_mode() == mode
        return self.trigger_mode

    def _get_storage_mode(self):
        wStorageMode = C.c_uint16()
        dll.get_storage_mode(self.camera_handle, wStorageMode)
        storage_mode_names = {0: "recorder",
                              1: "FIFO_buffer"}
        if self.verbose:
            print(" Storage mode:", storage_mode_names[wStorageMode.value])
        self.storage_mode = storage_mode_names[wStorageMode.value]
        return self.storage_mode

    def _set_storage_mode(self, mode="recorder"):
        storage_mode_numbers = {"recorder": 0,
                                "FIFO_buffer": 1}
        if self.verbose: print(" Setting storage mode to:", mode)
        wStorageMode = C.c_uint16(storage_mode_numbers[mode])
        dll.set_storage_mode(self.camera_handle, wStorageMode)
        assert self._get_storage_mode() == mode
        return self.storage_mode

    def _get_recorder_submode(self):
        wRecSubmode = C.c_uint16(1)
        dll.get_recorder_submode(self.camera_handle, wRecSubmode)
        recorder_submode_names = {0: "sequence",
                                  1: "ring_buffer"}
        if self.verbose:
            print(" Recorder submode:",
                  recorder_submode_names[wRecSubmode.value])
        self.recorder_submode = recorder_submode_names[wRecSubmode.value]
        return self.recorder_submode

    def _set_recorder_submode(self, mode="ring_buffer"):
        recorder_mode_numbers = {
            "sequence": 0,
            "ring_buffer": 1}
        if self.verbose: print(" Setting recorder submode to:", mode)
        wRecSubmode = C.c_uint16(recorder_mode_numbers[mode])
        print(wRecSubmode)
        dll.set_recorder_submode(self.camera_handle, wRecSubmode)
        assert self._get_recorder_submode() == mode
        return self.recorder_submode

    def _get_acquire_mode(self):
        wAcquMode = C.c_uint16(0)
        dll.get_acquire_mode(self.camera_handle, wAcquMode)
        acquire_mode_names = {0: "auto",
                              1: "external_static",
                              2: "external_dynamic"}
        if self.verbose:
            print(" Acquire mode:", acquire_mode_names[wAcquMode.value])
        self.acquire_mode = acquire_mode_names[wAcquMode.value]
        return self.acquire_mode

    def _set_acquire_mode(self, mode='auto'):
        acquire_mode_numbers = {"auto": 0,
                                "external_static": 1,
                                "external_dynamic": 2}
        if self.verbose:
            print(" Setting acquire mode to:", mode)
        wAcquMode = C.c_uint16(acquire_mode_numbers[mode])
        dll.set_acquire_mode(self.camera_handle, wAcquMode.value)
        assert self._get_acquire_mode() == mode
        return self.acquire_mode

    def _get_pixel_rate(self):
        dwPixelRate = C.c_uint32(0)
        dll.get_pixel_rate(self.camera_handle, dwPixelRate)
        assert dwPixelRate.value != 0
        if self.verbose:
            print(" Pixel rate:", dwPixelRate.value)
        self.pixel_rate = dwPixelRate.value
        return self.pixel_rate

    def _get_exposure_time(self):
        dwDelay = C.c_uint32(0)
        wTimeBaseDelay = C.c_uint16(0)
        dwExposure = C.c_uint32(0)
        wTimeBaseExposure = C.c_uint16(1)
        dll.get_delay_exposure_time(
            self.camera_handle,
            dwDelay,
            dwExposure,
            wTimeBaseDelay,
            wTimeBaseExposure)
        time_base_mode_names = {0: "nanoseconds",
                                1: "microseconds",
                                2: "milliseconds"}
        if self.verbose:
            print(" Exposure:", dwExposure.value,
                  time_base_mode_names[wTimeBaseExposure.value])
            print(" Delay:", dwDelay.value,
                  time_base_mode_names[wTimeBaseDelay.value])
        """
        exposure is returned in microseconds
        """
        self.exposure_time = (dwExposure.value *
                              10.**(3*wTimeBaseExposure.value - 3))
        self.delay_time = dwDelay.value
        return self.exposure_time        

    def _get_roi(self):
        wRoiX0, wRoiY0, wRoiX1, wRoiY1 = (
            C.c_uint16(), C.c_uint16(),
            C.c_uint16(), C.c_uint16())
        dll.get_roi(self.camera_handle, wRoiX0, wRoiY0, wRoiX1, wRoiY1)
        if self.verbose:
            print(" Camera ROI:");
            print(" From pixel", wRoiX0.value, "to pixel", wRoiX1.value, "(left/right)")
            print(" From pixel", wRoiY0.value, "to pixel", wRoiY1.value, "(up/down)")
        self.roi = {
            'left': wRoiX0.value,
            'top': wRoiY0.value,
            'right': wRoiX1.value,
            'bottom': wRoiY1.value}
        return self.roi

    def _prepare_to_record_to_memory(self):
        pass

"""
DLL management
"""
try:
    dll = C.oledll.LoadLibrary("SC2_Cam")
    """
    If you get a WindowsError, read PCO_err.h to decypher it.
    """
except WindowsError:
    print("Failed to load SC2_Cam.dll")
    print("You need this to run pco.py")
    raise

"""
This command opens the next pco camera; if you want to have multiple
cameras, and pick which one you're opening, I'd have to implement
PCO_OpenCameraEx, which would require me to understand PCO_OpenStruct.
"""
dll.open_camera = dll.PCO_OpenCamera
dll.open_camera.argtypes = [C.POINTER(C.c_void_p), C.c_uint16]

dll.close_camera = dll.PCO_CloseCamera
dll.close_camera.argtypes = [C.c_void_p]

dll.get_sensor_format = dll.PCO_GetSensorFormat
dll.get_sensor_format.argtypes = [C.c_void_p, C.POINTER(C.c_uint16)]

dll.get_camera_health = dll.PCO_GetCameraHealthStatus
dll.get_camera_health.argtypes = [
    C.c_void_p,
    C.POINTER(C.c_uint32),
    C.POINTER(C.c_uint32),
    C.POINTER(C.c_uint32)]

dll.get_temperature = dll.PCO_GetTemperature
dll.get_temperature.argtypes = [
    C.c_void_p,
    C.POINTER(C.c_int16),
    C.POINTER(C.c_int16),
    C.POINTER(C.c_int16)]

dll.get_trigger_mode = dll.PCO_GetTriggerMode
dll.get_trigger_mode.argtypes = [C.c_void_p, C.POINTER(C.c_uint16)]

dll.get_storage_mode = dll.PCO_GetStorageMode
dll.get_storage_mode.argtypes = [C.c_void_p, C.POINTER(C.c_uint16)]

dll.get_recorder_submode = dll.PCO_GetRecorderSubmode
dll.get_recorder_submode.argtypes = [C.c_void_p, C.POINTER(C.c_uint16)]

dll.get_acquire_mode = dll.PCO_GetAcquireMode
dll.get_acquire_mode.argtypes = [C.c_void_p, C.POINTER(C.c_uint16)]

dll.get_pixel_rate = dll.PCO_GetPixelRate
dll.get_pixel_rate.argtypes = [C.c_void_p, C.POINTER(C.c_uint32)]

dll.get_delay_exposure_time = dll.PCO_GetDelayExposureTime
dll.get_delay_exposure_time.argtypes = [
    C.c_void_p,
    C.POINTER(C.c_uint32),
    C.POINTER(C.c_uint32),
    C.POINTER(C.c_uint16),
    C.POINTER(C.c_uint16)]

dll.get_roi = dll.PCO_GetROI
dll.get_roi.argtypes = [
    C.c_void_p,
    C.POINTER(C.c_uint16),
    C.POINTER(C.c_uint16),
    C.POINTER(C.c_uint16),
    C.POINTER(C.c_uint16)]

dll.reset_settings_to_default = dll.PCO_ResetSettingsToDefault
dll.reset_settings_to_default.argtypes = [C.c_void_p]

dll.set_recording_state = dll.PCO_SetRecordingState
dll.set_recording_state.argtypes = [C.c_void_p, C.c_uint16]

dll.remove_buffer = dll.PCO_RemoveBuffer
dll.remove_buffer.argtypes = [C.c_void_p]

dll.free_buffer = dll.PCO_FreeBuffer
dll.free_buffer.argtypes = [C.c_void_p, C.c_int16]

dll.set_sensor_format = dll.PCO_SetSensorFormat
dll.set_sensor_format.argtypes = [C.c_void_p, C.c_uint16]

dll.set_trigger_mode = dll.PCO_SetTriggerMode
dll.set_trigger_mode.argtypes = [C.c_void_p, C.c_uint16]

dll.set_recorder_submode = dll.PCO_SetRecorderSubmode
dll.set_recorder_submode.argtypes = [C.c_void_p, C.c_uint16]

dll.set_acquire_mode = dll.PCO_SetAcquireMode
dll.set_acquire_mode.argtypes = [C.c_void_p, C.c_uint16]

dll.set_storage_mode = dll.PCO_SetStorageMode
dll.set_storage_mode.argtypes = [C.c_void_p, C.c_uint16]

if __name__ == '__main__':
    camera = Edge()
    camera.apply_settings()
    camera.close()
