export enum IDDocumentType {
  Passport = "passport",
  DriverLicense = "driver_license",
  NationalId = "national_id",
}

export interface Client {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phoneNumber: string;
  address: string;
  city: string;
  state: string;
  country: string;
  postalCode: string;
  dateOfBirth: string;
  idDocumentType: IDDocumentType;
  idDocumentNumber: string;
}
