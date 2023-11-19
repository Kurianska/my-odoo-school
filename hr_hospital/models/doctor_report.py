from odoo import models


class DoctorReport(models.AbstractModel):
    _name = 'report.hr_hospital.report_hr_hospital_doctor'
    _description = 'Hospital Doctor Report'

    def _get_report_values(self, docids, data=None):
        doc = self.env['hr.hospital.doctor'].browse(docids[0])

        return {
            'doc': doc,
        }
